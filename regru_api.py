# Документация от рег.ру
# https://developers.cloudvps.reg.ru/reglets/index.html
from enum import Enum

import requests

import settings


class Action(Enum):
    START = "start"
    STOP = "stop"


class Statuses(Enum):
    new = ("создается", "🤌")
    active = ("запущен", "🟢")
    off = ("опущен", "🔴")
    suspended = ("приостановлен", "💰")
    archive = ("удален", "❗️")

    def __init__(self, desc: str, emoji: str):
        self.desc = desc
        self.emoji = emoji


class RegClient:
    def __init__(self):
        self.root = "https://api.cloudvps.reg.ru/v1/"
        self.headers = {
            "Authorization": f"Bearer {settings.REGRU_TOKEN}",
            "Content-Type": "application/json",
        }

    def _get(self, path: str) -> dict:
        response = requests.get(f"{self.root}{path}", headers=self.headers)
        return response.json()

    def _post(self, path: str, payload: dict):
        response = requests.post(
            f"{self.root}{path}", headers=self.headers, json=payload
        )
        return response.json()

    def reglets(self):
        return self._get("reglets")

    def info(self, reglet_id: int):
        return self._get(f"reglets/{reglet_id}")

    def actions(self, reglet_id: int, action: Action):
        return self._post(
            f"reglets/{reglet_id}/actions", payload={"type": action.value}
        )


class RegletInfo:
    def __init__(self, info: dict):
        self.info = info

    @property
    def status(self) -> Statuses:
        return Statuses[self.info["reglet"]["status"]]

    @property
    def ip(self) -> str:
        return self.info["reglet"]["ip"].replace(".", "\.")

    @property
    def name(self) -> str:
        return self.info["reglet"]["name"]



client = RegClient()

if __name__ == "__main__":
    s = {1: {"key": 123}}
    print(s[1]["key"])
