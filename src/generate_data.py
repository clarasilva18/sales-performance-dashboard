"""Generate a fictional sales dataset (data/sales_sample.csv).

All data is made up for practice and portfolio purposes.
Run from the project root:  python src/generate_data.py
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

OUTPUT_FILE = Path(__file__).resolve().parent.parent / "data" / "sales_sample.csv"

# product -> unit price (R$), invented values
PRODUCTS = {
    "Notebook": 3200,
    "Smartphone": 1800,
    "Monitor": 900,
    "Bluetooth Headset": 250,
    "Keyboard": 180,
    "Mouse": 90,
}
CUSTOMERS = ["Ana", "Bruno", "Carla", "Diego", "Elisa", "Fabio", "Gabriela", "Hugo"]

START_DATE = date(2026, 6, 1)
END_DATE = date(2026, 9, 28)
NUM_SALES = 120


def generate_rows(seed: int = 42) -> list[list]:
    """Return a list of random sales rows, sorted by date."""
    random.seed(seed)  # same data every run
    total_days = (END_DATE - START_DATE).days
    rows = []
    for _ in range(NUM_SALES):
        sale_date = START_DATE + timedelta(days=random.randint(0, total_days))
        product = random.choice(list(PRODUCTS))
        quantity = random.randint(1, 3)
        revenue = quantity * PRODUCTS[product]
        rows.append([sale_date.isoformat(), product, quantity, revenue, random.choice(CUSTOMERS)])
    return sorted(rows, key=lambda row: row[0])


def main() -> None:
    rows = generate_rows()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "product", "quantity", "revenue", "customer"])
        writer.writerows(rows)
    print(f"Created {OUTPUT_FILE.name} with {len(rows)} sales.")


if __name__ == "__main__":
    main()
