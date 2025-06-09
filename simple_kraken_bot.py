import os
import csv
import time
from datetime import datetime
from decimal import Decimal, ROUND_DOWN

from dotenv import load_dotenv
import krakenex

INTERVAL = 120  # seconds
PAIR = "XBTUSD"  # trading pair on Kraken
TRANSACTIONS_FILE = "transactions.csv"

load_dotenv()
API_KEY = os.getenv("KRAKEN_API_KEY")
API_SECRET = os.getenv("KRAKEN_API_SECRET")

client = krakenex.API(key=API_KEY, secret=API_SECRET)


def get_balance(asset="ZUSD"):
    """Return available balance for the given asset."""
    try:
        resp = client.query_private("Balance")
        balance = resp["result"].get(asset, "0")
        return Decimal(balance)
    except Exception:
        return Decimal("0")


def load_open_transactions():
    """Load transactions marked as open from CSV."""
    orders = {}
    if os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, newline="") as f:
            for row in csv.DictReader(f):
                if row.get("status", "open") == "open":
                    orders[row["txid"]] = row
    return orders


def write_transaction(txid, side, volume, price, status="open"):
    write_header = not os.path.exists(TRANSACTIONS_FILE)
    with open(TRANSACTIONS_FILE, "a", newline="") as f:
        fieldnames = ["timestamp", "txid", "side", "volume", "price", "status"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.utcnow().isoformat(),
            "txid": txid,
            "side": side,
            "volume": volume,
            "price": price,
            "status": status,
        })


def update_transaction_status(txid, status):
    if not os.path.exists(TRANSACTIONS_FILE):
        return
    rows = []
    with open(TRANSACTIONS_FILE, newline="") as f:
        rows = list(csv.DictReader(f))
    with open(TRANSACTIONS_FILE, "w", newline="") as f:
        fieldnames = ["timestamp", "txid", "side", "volume", "price", "status"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if row["txid"] == txid:
                row["status"] = status
            writer.writerow(row)


def refresh_open_orders(orders):
    if not orders:
        return
    try:
        resp = client.query_private("OpenOrders")
        open_txids = set(resp["result"].get("open", {}).keys())
        for txid in list(orders.keys()):
            if txid not in open_txids:
                update_transaction_status(txid, "closed")
                orders.pop(txid, None)
    except Exception:
        pass


def get_ticker_price(pair=PAIR):
    try:
        data = client.query_public("Ticker", {"pair": pair})
        price = data["result"][list(data["result"])[0]]["c"][0]
        return Decimal(price)
    except Exception:
        return Decimal("0")


def round_volume(vol, precision=5):
    q = Decimal(vol).quantize(Decimal("1e-" + str(precision)), rounding=ROUND_DOWN)
    return str(q.normalize())


def place_limit_order(side, volume, price, pair=PAIR):
    params = {
        "pair": pair,
        "type": side,
        "ordertype": "limit",
        "price": str(price),
        "volume": volume,
    }
    resp = client.query_private("AddOrder", params)
    if resp.get("error"):
        print("Order error", resp["error"])
        return None
    txid = resp["result"]["txid"][0]
    write_transaction(txid, side, volume, price)
    return txid


def trading_loop():
    while True:
        balance = get_balance()
        open_orders = load_open_transactions()
        refresh_open_orders(open_orders)

        if not open_orders and balance > Decimal("20"):
            price = get_ticker_price()
            if price > 0:
                buy_price = price * Decimal("0.99")
                volume = round_volume(balance / buy_price)
                txid = place_limit_order("buy", volume, buy_price)
                if txid:
                    print("Placed buy order", txid)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    trading_loop()
