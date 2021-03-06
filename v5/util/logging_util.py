import logging
from enum import Enum
from typing import Optional, Union
from sys import stdout


__all__ = (
    'Logger',
    'LogLevels',
    'getLogger'
)

# Logger class
Logger = logging.Logger

# Set formatter depends on colorlog installation (optionals).
try:
    from colorlog import ColoredFormatter
    _Formatter = ColoredFormatter(
            "{log_color}[{name}] [{levelname}] [{asctime}] : {message}",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white,bold',
            },
            secondary_log_colors={},
            style='{'
    )
except ImportError:
    _Formatter = logging.Formatter(
        "[{name}] [{levelname}] [{asctime}] : {message}",
        style='{'
    )


class LogLevels(Enum):
    # CRITICAL level
    CRITICAL = logging.CRITICAL
    FATAL = CRITICAL    # alias for CRITICAL
    # ERROR level
    ERROR = logging.ERROR
    # WARNING level
    WARNING = logging.WARNING
    WARN = WARNING      # alias for WARNING
    # INFO level
    INFO = logging.INFO
    # DEBUG level
    DEBUG = logging.DEBUG


def getLogger(name: str, level: Optional[Union[LogLevels, int]] = LogLevels.DEBUG, formatter: logging.Formatter = _Formatter) -> Logger:
    if isinstance(level, LogLevels):
        level = level.value
    logger = logging.getLogger(name)
    logger.propagate = False    # Make child logger not use parent's logging handlers. - prevent log duplicates
    logger.setLevel(level)
    if not logger.handlers:
        console_handler = logging.StreamHandler(stream=stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger


