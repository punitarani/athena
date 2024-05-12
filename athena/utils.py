"""athena/utils.py"""

import logging

import pandas as pd

from athena.config import DATA_DIR, LOGS_DIR

SANITIZED_NAMES_FP = DATA_DIR.joinpath("sanitized_names.csv")
SANITIZED_NAMES_FP.touch(exist_ok=True)


LOGGERS = {}  # Logger cache


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The logger.
    """
    if name in LOGGERS:
        return LOGGERS[name]

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create file handler
    fh = logging.FileHandler(LOGS_DIR.joinpath(f"{name}.log"))
    fh.setLevel(logging.DEBUG)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    # Cache the logger
    LOGGERS[name] = logger

    return logger


def sanitize_name(text: str) -> str:
    """
    Sanitizes a string for use as a filename.
    Replace any non-alphanumeric characters with underscores.

    Args:
        text (str): The input string to sanitize.

    Returns:
        str: A sanitized, file-safe name.
    """
    name = "".join(c if c.isalnum() else "_" for c in text)
    save_sanitized_name(text, name)
    return name


def save_sanitized_name(text: str, name: str) -> None:
    """
    Save a sanitized name to a file in the data directory.

    Args:
        text (str): The original text.
        name (str): The sanitized name.
    """

    columns = ["text", "name"]

    # Read the existing data, or create a new DataFrame if the file is empty
    try:
        df = pd.read_csv(SANITIZED_NAMES_FP, encoding="utf-8", names=columns)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=columns)

    # Check for duplicates based on both `text` and `name`
    if not ((df["text"] == text) & (df["name"] == name)).any():
        # Append without reading the entire file again
        df_new = pd.DataFrame([[text, name]], columns=["text", "name"])
        df_new.to_csv(
            SANITIZED_NAMES_FP, mode="a", header=False, index=False, encoding="utf-8"
        )


def get_original_text(name: str) -> str | None:
    """
    Retrieves the original text given a sanitized name.

    Args:
        name (str): The sanitized name.

    Returns:
        str: The original text corresponding to the sanitized name if found, else None.
    """
    try:
        df = pd.read_csv(SANITIZED_NAMES_FP, encoding="utf-8")
        match = df[df["name"] == name]
        if not match.empty:
            return match.iloc[0]["text"]
    except pd.errors.EmptyDataError:
        pass
    return None
