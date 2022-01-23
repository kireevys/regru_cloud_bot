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

    def info(self):
        return self._get("reglets/1365929")

    def actions(self, action: Action):
        return self._post("reglets/1365929/actions", payload={"type": action.value})


class RegletInfo:
    def __init__(self, info: dict):
        self.info = info

    def status(self) -> Statuses:
        return Statuses[self.info["reglet"]["status"]]

    def ip(self) -> str:
        return self.info["reglet"]["ip"].replace(".", "\.")


client = RegClient()

if __name__ == "__main__":
    print(client.info())
