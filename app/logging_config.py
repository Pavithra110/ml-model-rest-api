import logging
from logging.handlers import RotatingFileHandler
from app.config import settings

logger = logging.getLogger("ml_api")

log_level = getattr(logging, settings.LOG_LEVEL.upper())

logger.setLevel(log_level)

console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)

file_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=5_000_000,
    backupCount=3
)

file_handler.setLevel(log_level)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)