import pandas as pd
import config 

from ga_optimizer import run_ga

# Load datasets
employees_24 = pd.read_csv(config.DATA_SMALL_PATH)
employees_65 = pd.read_csv(config.DATA_LARGE_PATH)

print('=' * 60)
print('Running GA for 24 Employees')
print('=' * 60)

result24 = run_ga(
    employee_df=employees_24,
    config= config.GA_CONFIG
)

print(result24)

print()

print('=' * 60)
print('Running GA for 65 Employees')
print('=' * 60)

result65 = run_ga(
    employee_df = employees_65,
    config = config.GA_CONFIG
)

print(result65)