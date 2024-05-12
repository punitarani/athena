"""athena package"""

from dotenv import load_dotenv

from .config import PROJECT_PATH
from .secrets import Secrets

# Load .env
__loaded_env = load_dotenv(PROJECT_PATH.joinpath(".env"))
assert __loaded_env, "Could not load .env file"

SECRETS = Secrets.load()

__all__ = ["SECRETS"]
