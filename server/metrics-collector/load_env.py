"""
load_env.py — import at top of detect_anomaly.py to load .env
Usage: import load_env  (no other code needed)
"""
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))