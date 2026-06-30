import logging
from pathlib import Path
from typing import Final

# =========================
# Configuration
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / 'data' / 'raw_data' / 'dataset.xlsx'
DATA_SMALL_PATH: Final[Path] = BASE_DIR / 'data' / 'processed_data' / 'dataset_small.csv'
DATA_LARGE_PATH: Final[Path] = BASE_DIR / 'data' / 'processed_data' / 'dataset_large.csv'

# Scheduling Parameters
SCHEDULING_DAYS = 7
SHIFTS = ['Morning', 'Afternoon', 'Evening']
SHIFT_HOURS = 8
MAX_HOURS_PER_WEEK = 40
RANDOM_SEED = 42
SMALL_DATASET_EMPLOYEES = 24
LARGE_DATASET_EMPLOYEES = 65

GA_CONFIG = {
    "population_size": 50,
    "crossover_rate": 0.8,
    "mutation_rate": 0.10,
    "elite_size": 2,
    "tournament_size": 3,
    "max_generations": 200,
    "early_stop": 30,
    "max_weekly_hours": 40,

    # Shift demand per day
    "shift_demand": {
        "Morning": 6,
        "Afternoon": 5,
        "Evening": 4
    }
}

# =========================
# Logging
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
)
logger = logging.getLogger(__name__)