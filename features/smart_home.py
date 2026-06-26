"""
KIRA — Smart Home Controller
Lights, AC, devices via WiFi
"""

import os
import json
import httpx
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
DEVICES_FILE = DATA_DIR / "devices.json"


class SmartHomeManager:
    def __init__(self):
        self._load()

    def _load(self):
        if DEVICES_FILE.exists():
            with open(DEVICES_FILE) as f:
                self.devices = json.load(f)
        else:
            self.devices = {}
            self._save()

    def _save(self):
        with open(DEVICES_FILE, "w") as f:
            json.dump(self.devices, f, indent=2)

    def add_device(self, name: str, device_type: str, ip: str, api_url: str = "") -> str:
        self.devices[name.lower()] = {
            "name": name,
            "type": device_type,
            "ip": ip,
            "api_url": api_url,
            "status": "unknown"
        }
        self._save()
        return f"{name} add ho gaya"

    async def control_device(self, name: str, action: str, value: str = "") -> str:
        device = self.devices.get(name.lower())
        if not device:
            return f"{name} nahi mila, pehle add karo"

        try:
            # Generic HTTP device control
            if device.get("api_url"):
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        device["api_url"],
                        json={"action": action, "value": value},
                        timeout=5.0
                    )
                    if response.status_code == 200:
                        device["status"] = action
                        self._save()
                        return f"{name} {action} ho gaya"

            # Simulate for testing
            device["status"] = action
            self._save()
            return f"{name} {action} ho gaya"

        except Exception as e:
            return f"{name} se connect nahi ho paya — WiFi check karo"

    async def turn_on(self, device_name: str) -> str:
        return await self.control_device(device_name, "on")

    async def turn_off(self, device_name: str) -> str:
        return await self.control_device(device_name, "off")

    async def set_temperature(self, device_name: str, temp: int) -> str:
        return await self.control_device(device_name, "temperature", str(temp))

    async def set_brightness(self, device_name: str, level: int) -> str:
        return await self.control_device(device_name, "brightness", str(level))

    def get_all_devices(self) -> list:
        return list(self.devices.values())

    def get_device_status(self, name: str) -> str:
        device = self.devices.get(name.lower())
        if device:
            return f"{device['name']}: {device['status']}"
        return f"{name} nahi mila"

    async def home_mode(self, mode: str) -> str:
        """Set home mode — ghar, bahar, sleep"""
        results = []
        if mode == "sleep":
            for name in self.devices:
                d = self.devices[name]
                if d["type"] == "light":
                    results.append(await self.turn_off(name))
                elif d["type"] == "ac":
                    results.append(await self.set_temperature(name, 26))
        elif mode == "home":
            for name in self.devices:
                d = self.devices[name]
                if d["type"] == "light":
                    results.append(await self.turn_on(name))
                elif d["type"] == "ac":
                    results.append(await self.turn_on(name))
        elif mode == "away":
            for name in self.devices:
                results.append(await self.turn_off(name))

        return f"Home {mode} mode on — {len(results)} devices"


smart_home = SmartHomeManager()
