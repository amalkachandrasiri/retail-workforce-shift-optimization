import pandas as pd
import config 
import util
import evaluation as eval
import visualization as vs

from ga_optimizer import run_ga
from mip_optimizer import run_mip

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

print()

print('=' * 60)
print('Running GA for 24 Employees')
print('=' * 60)

result24_ga = run_ga(employees_24, config.GA_CONFIG, 24)

print()

print('=' * 60)
print('Running GA for 65 Employees')
print('=' * 60)

result65_ga = run_ga(employees_65, config.GA_CONFIG, 65)

print('=' * 60)
print('Running MIP for 24 Employees')
print('=' * 60)

result24_mip = run_mip(employees_24, config.GA_CONFIG, 24)

print()

print('=' * 60)
print('Running MIP for 65 Employees')
print('=' * 60)

result65_mip = run_mip(employees_65, config.GA_CONFIG, 65)

# ===============================
# roaster demostration 
# ===============================
print('=' * 60)
print('Roaster - 24 Employess - GA Results ')
print('=' * 60)
#print(result24)
util.display_roster(result24_ga['schedule'], config.EMP_ROASTER_24_GA)

print()

print('=' * 60)
print('Roaster - 65 Employess -  - GA Results')
print('=' * 60)
util.display_roster(result65_ga['schedule'], config.EMP_ROASTER_65_GA)

print()

print('=' * 60)
print('Roaster - 24 Employess - MIP Results ')
print('=' * 60)
util.display_roster(result24_mip['schedule'], config.EMP_ROASTER_24_MIP)

print()

print('=' * 60)
print('Roaster - 65 Employess - MIP Results ')
print('=' * 60)
util.display_roster(result65_mip['schedule'], config.EMP_ROASTER_65_MIP)

# ===============================
# Analysis
# ===============================

ga_metrics_25 = eval.evaluate_schedule(result24_ga)
util.print_summary('GA - 24 Employees', ga_metrics_25)

ga_metrics_65 = eval.evaluate_schedule(result65_ga)
util.print_summary('GA - 65 Employees', ga_metrics_65)

mip_metrics_24 = eval.evaluate_schedule(result24_mip)
util.print_summary('MIP - 24 Employees', mip_metrics_24)

mip_metrics_65 = eval.evaluate_schedule(result65_mip)
util.print_summary('MIP - 65 Employees', mip_metrics_65)

# ===============================
# Visualization 
# ===============================

vs.plot_labour_cost_comparison(ga_metrics_25, mip_metrics_24, ga_metrics_65, mip_metrics_65)
vs.plot_execution_time_comparison(ga_metrics_25, mip_metrics_24, ga_metrics_65, mip_metrics_65)



