# language: Python, file: config.py
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN     = os.getenv("BOT_TOKEN")
HIBP_API_KEY  = os.getenv("HIBP_API_KEY")
FNS_API_KEY   = os.getenv("FNS_API_KEY")

HIBP_URL      = "https://haveibeenpwned.com/api/v3"
FNS_URL       = "https://api-fns.ru/api"
FSSP_URL      = "https://api-ip.fssprus.ru/api/v1.0"
KAD_URL       = "https://kad.arbitr.ru"
