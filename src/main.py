import pandas as pd
import config 
import matplotlib.pyplot as plt

from ga_optimizer import run_ga

import matplotlib.pyplot as plt


def plot_convergence(history_24, history_65):

    plt.figure(figsize=(10, 6))
    generations = [0,10,20,30,40,50,60,70,80,90,100]

    plt.plot(generations, history_24, label='24 Employees')
    plt.plot(generations, history_65, label='65 Employees')

    plt.title('GA Convergence Analysis')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # save report 
    plt.savefig(config.GA_CONVERGENCE_REPORT, dpi = 300, bbox_inches = 'tight')
    plt.show()

# Load datasets
employees_24 = pd.read_csv(config.DATA_SMALL_PATH)
employees_65 = pd.read_csv(config.DATA_LARGE_PATH)
'''
print('available_morning', employees_24['available_morning'].sum())
print('available_afternoon', employees_24['available_afternoon'].sum())
print('available_evening', employees_24['available_evening'].sum())

print('/n  65 dataset')

print('available_morning', employees_65['available_morning'].sum())
print('available_afternoon', employees_65['available_afternoon'].sum())
print('available_evening', employees_65['available_evening'].sum())
'''
print('=' * 60)
print('Running GA for 24 Employees')
print('=' * 60)
best_24, history_24 = run_ga(employees_24, config.GA_CONFIG, 24)
print()
print('=' * 60)
print('Running GA for 65 Employees')
print('=' * 60)
best_65, history_65 = run_ga(employees_65, config.GA_CONFIG, 65)

plot_convergence(history_24, history_65)


