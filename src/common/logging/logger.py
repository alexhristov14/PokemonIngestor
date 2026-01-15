import logging
import sys
from logging.config import dictConfig
from typing import Optional

LOG_LEVEL = "INFO"
SERVICE_NAME = "data-platform"


def setup_logging(
    level: Optional[str] = None,
    json_logs: bool = True,
) -> None:
    """
    Configure application-wide logging.
    Call ONCE at application startup.
    """

    log_level = level or LOG_LEVEL

    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        }
    }

    if json_logs:
        handlers["console"]["formatter"] = "json"
    else:
        handlers["console"]["formatter"] = "default"

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {"format": ("%(asctime)s | %(levelname)s | %(name)s | " "%(message)s")},
                "json": {"()": "common.logging.json_formatter.JSONFormatter"},
            },
            "handlers": handlers,
            "root": {
                "level": log_level,
                "handlers": ["console"],
            },
            "loggers": {
                # Silence noisy libs
                "urllib3": {"level": "WARNING"},
                "elasticsearch": {"level": "WARNING"},
                "cassandra": {"level": "WARNING"},
                "asyncio": {"level": "WARNING"},
            },
        }
    )
