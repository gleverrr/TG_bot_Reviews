import os
from dotenv import load_dotenv
import logging
load_dotenv()
logging.basicConfig(level=logging.INFO)
class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    DATABASE_URL = os.getenv('DATABASE_URL')
