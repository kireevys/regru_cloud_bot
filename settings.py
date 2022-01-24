import logging.config
import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
REGRU_TOKEN = os.getenv("REGRU_TOKEN")
MASTER_GROUP_ID = os.getenv("MASTER_GROUP_ID")
REGLET_ID = os.getenv("REGLET_ID")

LOGGING = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s] | %(name)+12s | %(funcName)+15s:%(lineno)s | %(levelname)-8s | %(message)s"
        }
    },
    "handlers": {
        "stream": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "app_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "simple",
            "filename": "mr_brigg.log",  # noqa
            "utc": True,
            "when": "midnight",
        },
    },
    "loggers": {
        "": {
            "handlers": ["stream", "app_file"],
            "level": logging.INFO,
        },
    },
}

logging.config.dictConfig(LOGGING)
