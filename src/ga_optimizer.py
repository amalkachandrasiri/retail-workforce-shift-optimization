import random
import pandas as pd

def create_daily_schedule(employee_df, config):
    ...

def create_random_chromosome(employee_df, config):

    chromosome = []

    for day in range(7):

        daily_schedule = create_daily_schedule(
            employee_df,
            config
        )

        chromosome.extend(daily_schedule)

    return chromosome

def initialize_population(employee_df, config):

    population = []

    for _ in range(config["population_size"]):

        chromosome = create_random_chromosome(
            employee_df,
            config
        )

        population.append(chromosome)

    return population


def run_ga(employee_df, config):
    '''
    Runs the complete Genetic Algorithm.
    '''
    
    print(f'Employees : {len(employee_df)}')

    population = initialize_population(
        employee_df,
        config
    )    

    print(f'Population Created : {len(population)}')

    return {
        'population_size': len(population)
    }
    
