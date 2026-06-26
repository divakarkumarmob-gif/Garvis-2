"""
KIRA — Finance Tracker
Expenses, budget, payments
"""

import json
import time
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
FINANCE_FILE = DATA_DIR / "finance.json"


class FinanceTracker:
    def __init__(self):
        self._load()

    def _load(self):
        if FINANCE_FILE.exists():
            with open(FINANCE_FILE) as f:
                self.data = json.load(f)
        else:
            self.data = {
                "expenses": [],
                "income": [],
                "pending_payments": [],
                "monthly_budget": 0
            }
            self._save()

    def _save(self):
        with open(FINANCE_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def add_expense(self, amount: float, category: str, note: str = "") -> str:
        self.data["expenses"].append({
            "amount": amount,
            "category": category,
            "note": note,
            "date": time.strftime("%Y-%m-%d"),
            "time": time.time()
        })
        self._save()
        today_total = self.get_today_total()
        return f"₹{amount} add ho gaya — aaj ka total: ₹{today_total}"

    def add_income(self, amount: float, source: str = "") -> str:
        self.data["income"].append({
            "amount": amount,
            "source": source,
            "date": time.strftime("%Y-%m-%d")
        })
        self._save()
        return f"₹{amount} income add ho gayi"

    def add_pending_payment(self, name: str, amount: float, due_date: str = "") -> str:
        self.data["pending_payments"].append({
            "name": name,
            "amount": amount,
            "due_date": due_date,
            "paid": False
        })
        self._save()
        return f"{name} ka ₹{amount} pending add ho gaya"

    def mark_paid(self, name: str) -> str:
        for p in self.data["pending_payments"]:
            if p["name"].lower() == name.lower() and not p["paid"]:
                p["paid"] = True
                self._save()
                return f"{name} ka payment done!"
        return f"{name} nahi mila"

    def set_budget(self, amount: float) -> str:
        self.data["monthly_budget"] = amount
        self._save()
        return f"Monthly budget ₹{amount} set ho gaya"

    def get_today_total(self) -> float:
        today = time.strftime("%Y-%m-%d")
        return sum(e["amount"] for e in self.data["expenses"] if e["date"] == today)

    def get_monthly_total(self) -> float:
        month = time.strftime("%Y-%m")
        return sum(e["amount"] for e in self.data["expenses"] if e["date"].startswith(month))

    def get_pending_payments(self) -> list:
        return [p for p in self.data["pending_payments"] if not p["paid"]]

    def get_summary(self) -> str:
        today = self.get_today_total()
        month = self.get_monthly_total()
        pending = self.get_pending_payments()
        budget = self.data["monthly_budget"]

        summary = f"Aaj: ₹{today}, Mahina: ₹{month}"
        if budget:
            remaining = budget - month
            summary += f", Budget baki: ₹{remaining}"
        if pending:
            summary += f", Pending: {len(pending)} payments"
        return summary


finance_tracker = FinanceTracker()
