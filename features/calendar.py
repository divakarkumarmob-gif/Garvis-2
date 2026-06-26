"""
KIRA — Calendar & Reminders
Events, birthdays, tasks
"""

import json
import time
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
CALENDAR_FILE = DATA_DIR / "calendar.json"


class CalendarManager:
    def __init__(self):
        self._load()

    def _load(self):
        if CALENDAR_FILE.exists():
            with open(CALENDAR_FILE) as f:
                self.data = json.load(f)
        else:
            self.data = {
                "events": [],
                "birthdays": [],
                "tasks": [],
                "reminders": []
            }
            self._save()

    def _save(self):
        with open(CALENDAR_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def add_event(self, title: str, date: str, time_str: str = "", note: str = "") -> str:
        self.data["events"].append({
            "title": title,
            "date": date,
            "time": time_str,
            "note": note,
            "created": time.time()
        })
        self._save()
        return f"Event add ho gaya — {title} on {date}"

    def add_birthday(self, name: str, date: str) -> str:
        self.data["birthdays"].append({
            "name": name,
            "date": date
        })
        self._save()
        return f"{name} ki birthday yaad kar li — {date}"

    def add_task(self, task: str, due: str = "") -> str:
        self.data["tasks"].append({
            "task": task,
            "due": due,
            "done": False,
            "created": time.time()
        })
        self._save()
        return f"Task add ho gaya — {task}"

    def complete_task(self, task_index: int) -> str:
        if 0 <= task_index < len(self.data["tasks"]):
            self.data["tasks"][task_index]["done"] = True
            self._save()
            return "Task complete ho gaya!"
        return "Task nahi mila"

    def add_reminder(self, text: str, time_str: str) -> str:
        self.data["reminders"].append({
            "text": text,
            "time": time_str,
            "done": False
        })
        self._save()
        return f"Reminder set ho gaya — {text} at {time_str}"

    def get_today_events(self) -> list:
        today = time.strftime("%Y-%m-%d")
        return [e for e in self.data["events"] if e["date"] == today]

    def get_upcoming_birthdays(self, days: int = 7) -> list:
        today = time.strftime("%m-%d")
        upcoming = []
        for b in self.data["birthdays"]:
            try:
                bday = b["date"][5:]  # MM-DD
                if bday >= today:
                    upcoming.append(b)
            except Exception:
                pass
        return upcoming[:5]

    def get_pending_tasks(self) -> list:
        return [t for t in self.data["tasks"] if not t["done"]]

    def get_morning_briefing(self) -> str:
        events = self.get_today_events()
        tasks = self.get_pending_tasks()
        birthdays = self.get_upcoming_birthdays(1)

        parts = []
        if birthdays:
            parts.append(f"Birthday: {birthdays[0]['name']}")
        if events:
            parts.append(f"Events: {len(events)} aaj")
        if tasks:
            parts.append(f"Tasks: {len(tasks)} pending")

        return ", ".join(parts) if parts else "Aaj koi events nahi"


calendar_manager = CalendarManager()
