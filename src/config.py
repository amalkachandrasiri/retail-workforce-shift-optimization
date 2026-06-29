'''
config.py 
'''

import logging
from pathlib import Path
from typing import Final

# =========================
# Configuration
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / 'data' / 'raw_data' / 'dataset.xlsx'
DATA_SMALL_PATH: Final[Path] = BASE_DIR / 'data' / 'processed_data' / 'dataset_small.xlsx'
DATA_LARGE_PATH: Final[Path] = BASE_DIR / 'data' / 'processed_data' / 'dataset_large.xlsx'

# Scheduling Parameters
SCHEDULING_DAYS = 7
SHIFTS = ['Morning', 'Afternoon', 'Evening']
SHIFT_HOURS = 8
MAX_HOURS_PER_WEEK = 40
RANDOM_SEED = 42
SMALL_DATASET_EMPLOYEES = 24
LARGE_DATASET_EMPLOYEES = 65

# =========================
# Logging
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
)
logger = logging.getLogger(__name__)