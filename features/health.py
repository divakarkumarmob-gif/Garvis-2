"""
KIRA — Health Tracker
Medicine reminders, fitness, mental health
"""

import json
import time
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
HEALTH_FILE = DATA_DIR / "health.json"


class HealthTracker:
    def __init__(self):
        self._load()

    def _load(self):
        if HEALTH_FILE.exists():
            with open(HEALTH_FILE) as f:
                self.data = json.load(f)
        else:
            self.data = {
                "medicines": [],
                "water_count": 0,
                "water_date": "",
                "mood_log": [],
                "sleep_log": [],
                "steps": 0,
                "weight_log": [],
                "symptoms": []
            }
            self._save()

    def _save(self):
        with open(HEALTH_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def add_medicine(self, name: str, time_str: str, dose: str = "") -> str:
        self.data["medicines"].append({
            "name": name,
            "time": time_str,
            "dose": dose,
            "added": time.time()
        })
        self._save()
        return f"{name} reminder set ho gaya — {time_str}"

    def log_water(self) -> str:
        today = time.strftime("%Y-%m-%d")
        if self.data["water_date"] != today:
            self.data["water_count"] = 0
            self.data["water_date"] = today
        self.data["water_count"] += 1
        self._save()
        count = self.data["water_count"]
        if count < 8:
            return f"Paani {count} baar piya aaj — {8 - count} aur peeo"
        return f"Paani {count} baar piya — accha hai!"

    def log_mood(self, mood: str, note: str = "") -> str:
        self.data["mood_log"].append({
            "mood": mood,
            "note": note,
            "time": time.time()
        })
        self._save()
        return f"Mood note ho gaya — {mood}"

    def log_sleep(self, hours: float) -> str:
        self.data["sleep_log"].append({
            "hours": hours,
            "date": time.strftime("%Y-%m-%d")
        })
        self._save()
        if hours < 6:
            return f"{hours} ghante soye — kam hai boss, 7-8 ghante chahiye"
        elif hours > 9:
            return f"{hours} ghante soye — thoda zyada ho gaya"
        return f"{hours} ghante soye — accha hai!"

    def log_weight(self, weight: float) -> str:
        self.data["weight_log"].append({
            "weight": weight,
            "date": time.strftime("%Y-%m-%d")
        })
        self._save()
        return f"{weight} kg note ho gaya"

    def get_medicines(self) -> list:
        return self.data["medicines"]

    def get_summary(self) -> str:
        today = time.strftime("%Y-%m-%d")
        water = self.data["water_count"] if self.data["water_date"] == today else 0
        medicines = len(self.data["medicines"])
        recent_mood = self.data["mood_log"][-1]["mood"] if self.data["mood_log"] else "unknown"
        return f"Paani: {water} baar, Medicines: {medicines}, Mood: {recent_mood}"


health_tracker = HealthTracker()
