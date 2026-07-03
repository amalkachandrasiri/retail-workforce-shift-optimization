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

# report paths 
EMP_ROASTER_24_GA : Final[Path] = BASE_DIR / 'reports' / 'emp_roaster_24_GA.csv'
EMP_ROASTER_65_GA : Final[Path] = BASE_DIR / 'reports' / 'emp_roaster_65_GA.csv'

EMP_ROASTER_24_MIP : Final[Path] = BASE_DIR / 'reports' / 'emp_roaster_24_MIP.csv'
EMP_ROASTER_65_MIP : Final[Path] = BASE_DIR / 'reports' / 'emp_roaster_65_MIP.csv'

# graphs paths
LABOUR_COST_GRAPH : Final[Path] = BASE_DIR / 'reports' / 'labour_cost_comparison.png'
EXC_TIME_GRAPH : Final[Path] = BASE_DIR / 'reports' / 'execution_time_comparison.png'



# Scheduling Parameters
SCHEDULING_DAYS = 7
SHIFTS = ['Morning', 'Afternoon', 'Evening']
SHIFT_HOURS = 8
MAX_HOURS_PER_WEEK = 40
RANDOM_SEED = 42
SMALL_DATASET_EMPLOYEES = 24
LARGE_DATASET_EMPLOYEES = 65

GA_CONFIG = {
    'population_size': 50,
    'crossover_rate': 0.8,
    'mutation_rate': 0.10,
    'elite_size': 2,
    'tournament_size': 3,
    'max_generations': 200,
    'early_stop': 30,
    'max_weekly_hours': 40,
    
    'shift_demand_24' : { 
    'Morning': 6,
    'Afternoon': 5,
    'Evening': 4
    },

    'shift_demand_65' : {
    'Morning': 15,
    'Afternoon': 13,
    'Evening': 10
    },

    # penalties 
    'penalties': {
        'unavailable': 1000,
        'duplicate_shift': 1000,
        'weekly_hours': 1000
    },

    'tournament_size': 3,   

    'crossover_probability': 0.8,
    'mutation_probability': 0.1,

    'elite_size': 2,

    "generations": 100,
}

# =========================
# Logging
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
)
logger = logging.getLogger(__name__)