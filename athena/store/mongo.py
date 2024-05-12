"""athena/store/mongo.py"""

from motor.motor_asyncio import AsyncIOMotorClient

from athena import SECRETS

MONGO_URI = f"mongodb+srv://{SECRETS.MONGO_USERNAME}:{SECRETS.MONGO_PASSWORD}@{SECRETS.MONGO_DB}.{SECRETS.MONGO_HOST}/?retryWrites=true&w=majority"
mongo_client = AsyncIOMotorClient(MONGO_URI)
