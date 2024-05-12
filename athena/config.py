"""athena/config.py"""

from pathlib import Path

PROJECT_PATH = Path(__file__).parents[1]

DATA_DIR = PROJECT_PATH.joinpath("data")
if not DATA_DIR.exists():
    DATA_DIR.mkdir()

PAPERS_DIR = DATA_DIR.joinpath("papers")
if not PAPERS_DIR.exists():
    PAPERS_DIR.mkdir()

LOGS_DIR = PROJECT_PATH.joinpath("logs")
if not LOGS_DIR.exists():
    LOGS_DIR.mkdir()

EMAIL = "email@gmail.com"
