"""
Configuration module for the Autonomous Generative Trading Strategies system.
Centralizes all configuration parameters, environment variables, and constants.
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

@dataclass
class FirebaseConfig:
    """Firebase configuration and initialization."""
    credential_path: str = "firebase_credentials.json"
    project_id: str = "autonomous-trading-system"
    
    @classmethod
    def initialize_firebase(cls) -> firestore.Client:
        """Initialize Firebase and return Firestore client."""
        try:
            if not firebase_admin._apps:
                if os.path.exists(cls.credential_path):
                    cred = credentials.Certificate(cls.credential_path)
                else:
                    # For development/testing, use application default credentials
                    cred = credentials.ApplicationDefault()
                
                firebase_admin.initialize_app(cred, {
                    'projectId': cls.project_id,
                })
            
            return firestore.client()
        except Exception as e:
            logging.error(f"Firebase initialization failed: {e}")
            raise

@dataclass
class TradingConfig:
    """Trading system configuration parameters."""
    # Data settings
    data_interval: str = "1h"  # 1 hour candles
    historical_days: int = 365  # 1 year of historical data
    symbols: List[str] = None  # Will be populated from env
    
    # Model settings
    strategy_generation_batch_size: int = 10
    max_strategies_per_generation: int = 50
    model_update_frequency_hours: int = 24
    
    # Backtesting settings
    backtest_initial_capital: float = 10000.0
    backtest_commission_rate: float = 0.001  # 0.1%
    backtest_slippage_rate: float = 0.0005  # 0.05%
    
    # Risk management
    max_position_size_pct: float = 0.1  # 10% of portfolio
    max_daily_loss_pct: float = 0.02  # 2% daily loss limit
    stop_loss_pct: float = 0.05  # 5% stop loss
    
    # Execution settings
    paper_trading: bool = True
    min_order_size_usd: float = 10.0
    max_open_positions: int = 5
    
    def __post_init__(self):
        """Initialize configuration from environment variables."""
        if self.symbols is None:
            symbols_str = os.getenv("TRADING_SYMBOLS", "BTC/USDT,ETH/USDT,ADA/USDT")
            self.symbols = [s.strip() for s in symbols_str.split(",")]
        
        self.paper_trading = os.getenv("PAPER_TRADING", "True").lower() == "true"

class StrategyParameters:
    """Strategy parameter definitions and constraints."""
    
    # Technical indicator parameters
    INDICATOR_PARAMS = {
        'sma_periods': {'min': 5, 'max': 200, 'step': 5},
        'ema_periods': {'min': 5, 'max': 100, 'step': 5},
        'rsi_period': {'min': 7, 'max': 21, 'step': 1},
        'macd_fast': {'min': 8, 'max': 21, 'step': 1},
        'macd_slow': {'min': 21, 'max': 55, 'step': 1},
        'bollinger_period': {'min': 10, 'max': 50, 'step': 5},
        'bollinger_std': {'min': 1.5, 'max': 3.0, 'step': 0.5},
    }
    
    # Entry/exit condition parameters
    CONDITION_PARAMS = {
        'thresholds': {'min': -5.0, 'max': 5.0, 'step': 0.1},
        'cross_periods': {'min': 1, 'max': 10, 'step': 1},
        'momentum_lookback': {'min': 3, 'max': 20, 'step': 1},
    }
    
    # Risk parameters
    RISK_PARAMS = {
        'position_size': {'min': 0.01, 'max': 0.5, 'step': 0.01},
        'take_profit': {'min': 0.01, 'max': 0.2, 'step': 0.01},
        'stop_loss': {'min': 0.005, 'max': 0.1, 'step': 0.005},
        'trailing_stop': {'min': 0.005, 'max': 0.05, 'step': 0.005},
    }

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('trading_system.log')
    ]
)

logger = logging.getLogger(__name__)

# Global configuration instance
config = TradingConfig()