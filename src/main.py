import pandas as pd
import config 

from ga_optimizer import run_ga

# Load datasets
employees_24 = pd.read_csv(config.DATA_SMALL_PATH)
employees_65 = pd.read_csv(config.DATA_LARGE_PATH)

print('=' * 60)
print('Running GA for 24 Employees')
print('=' * 60)

'''
print('available_morning', employees_24['available_morning'].sum())
print('available_afternoon', employees_24['available_afternoon'].sum())
print('available_evening', employees_24['available_evening'].sum())

print('/n  65 dataset')

print('available_morning', employees_65['available_morning'].sum())
print('available_afternoon', employees_65['available_afternoon'].sum())
print('available_evening', employees_65['available_evening'].sum())
'''

result24 = run_ga(employees_24, config.GA_CONFIG, 24)

# print(result24)

print()

print('=' * 60)
print('Running GA for 65 Employees')
print('=' * 60)

result65 = run_ga(employees_65, config.GA_CONFIG, 65)

# print(result65)

