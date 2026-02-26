"""
Real-time and historical market data ingestion module.
Handles data fetching, validation, preprocessing, and storage in Firebase.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import ccxt
from datetime import datetime, timedelta
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
from collections import deque

from trading_config import config, logger
from firebase_utils import FirebaseManager

class MarketDataIngestor:
    """
    Ingests market data from multiple exchanges in