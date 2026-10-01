"""Sales Performance Dashboard.

Reads a sales CSV, calculates key sales metrics (monthly revenue, average
ticket, goal progress, commission) and saves a 4-chart dashboard image.

Run from the project root:  python src/dashboard.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# ---------- Settings ----------
ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "sales_sample.csv"
OUTPUT_IMAGE = ROOT / "images" / "dashboard.png"

MONTHLY_GOAL = 70_000      # monthly sales goal (R$)
COMMISSION_RATE = 0.03     # 3% commission on revenue
# ------------------------------


def load_sales(path: Path) -> pd.DataFrame:
    """Load the sales CSV and add a 'month' column (e.g. 2026-09)."""
    sales = pd.read_csv(path, parse_dates=["date"])
    sales["month"] = sales["date"].dt.to_period("M")
    return sales


def calculate_metrics(sales: pd.DataFrame, goal: float, commission_rate: float) -> dict:
    """Calculate the main sales metrics and return them in a dictionary."""
    revenue_by_month = sales.groupby("month")["revenue"].sum()
    revenue_by_product = sales.groupby("product")["revenue"].sum().sort_values(ascending=False)

    latest_month = revenue_by_month.index[-1]
    latest_revenue = revenue_by_month.iloc[-1]

    return {
        "total_revenue": sales["revenue"].sum(),
        "average_ticket": sales["revenue"].mean(),
        "top_product": revenue_by_product.index[0],
        "latest_month": latest_month,
        "latest_revenue": latest_revenue,
        "goal_progress": latest_revenue / goal * 100,
        "remaining_to_goal": max(goal - latest_revenue, 0),
        "commission": latest_revenue * commission_rate,
        "revenue_by_month": revenue_by_month,
        "revenue_by_product": revenue_by_product,
    }


def print_summary(metrics: dict) -> None:
    """Print a short text summary in the terminal."""
    print("=" * 34)
    print("SALES SUMMARY")
    print("=" * 34)
    print(f"Total revenue:   R$ {metrics['total_revenue']:,.2f}")
    print(f"Average ticket:  R$ {metrics['average_ticket']:,.2f}")
    print(f"Top product:     {metrics['top_product']}")
    print(f"\nLatest month: {metrics['latest_month']}")
    print(f"  Revenue:       R$ {metrics['latest_revenue']:,.2f}")
    print(f"  Goal progress: {metrics['goal_progress']:.1f}%")
    print(f"  Remaining:     R$ {metrics['remaining_to_goal']:,.2f}")
    print(f"  Commission:    R$ {metrics['commission']:,.2f}")


def build_dashboard(sales: pd.DataFrame, metrics: dict, goal: float, output: Path) -> None:
    """Create the 4-chart dashboard and save it as an image."""
    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    fig.suptitle("Sales Performance Dashboard", fontsize=18, fontweight="bold")

    # 1) Revenue by month vs goal
    by_month = metrics["revenue_by_month"]
    axes[0, 0].bar(by_month.index.astype(str), by_month.values, color="#2E75B6")
    axes[0, 0].axhline(goal, color="red", linestyle="--", label="Monthly goal")
    axes[0, 0].set_title("Revenue by month")
    axes[0, 0].set_ylabel("R$")
    axes[0, 0].legend()

    # 2) Revenue by product
    by_product = metrics["revenue_by_product"]
    axes[0, 1].barh(by_product.index, by_product.values, color="#70AD47")
    axes[0, 1].invert_yaxis()
    axes[0, 1].set_title("Revenue by product")
    axes[0, 1].set_xlabel("R$")

    # 3) Daily revenue over time
    by_day = sales.groupby("date")["revenue"].sum()
    axes[1, 0].plot(by_day.index, by_day.values, color="#ED7D31", marker="o", markersize=3)
    axes[1, 0].set_title("Daily revenue")
    axes[1, 0].tick_params(axis="x", rotation=45)

    # 4) Goal progress for the latest month
    sold = metrics["latest_revenue"]
    remaining = metrics["remaining_to_goal"]
    if remaining > 0:
        axes[1, 1].pie([sold, remaining], labels=["Sold", "Remaining"], autopct="%1.0f%%",
                       colors=["#2E75B6", "#D9D9D9"])
    else:
        axes[1, 1].pie([1], labels=["Goal reached!"], colors=["#70AD47"])
    axes[1, 1].set_title(f"Goal progress - {metrics['latest_month']}")

    plt.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, dpi=150)
    plt.close(fig)


def main() -> None:
    sales = load_sales(DATA_FILE)
    metrics = calculate_metrics(sales, MONTHLY_GOAL, COMMISSION_RATE)
    print_summary(metrics)
    build_dashboard(sales, metrics, MONTHLY_GOAL, OUTPUT_IMAGE)
    print(f"\nDashboard saved to {OUTPUT_IMAGE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
