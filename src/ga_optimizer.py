import random
import copy
import pandas as pd
import time

# ==========================================
# 1. CHROMOSOME INITIALIZATION & CREATION
# ========================================== 

def create_daily_schedule(employee_df, config, day, dataset_size):
    '''
    Creates a valid daily schedule matching the exact shift demands.
    '''
    daily_schedule = []
    assigned_today = set()

    shift_columns = {
        'Morning': 'available_morning',
        'Afternoon': 'available_afternoon',
        'Evening': 'available_evening'
    }

    shift_demand = config['shift_demand_24'] if dataset_size == 24 else config['shift_demand_65']

    for shift, demand in shift_demand.items():
        # Filter for employees who are generally available for this shift
        available = employee_df[employee_df[shift_columns[shift]] == 1]

        # Prevent duplicate assignments on the exact same day during initialization
        available = available[~available['employee_id'].isin(assigned_today)]

        # Guard against insufficient staff configurations
        if len(available) < demand:
            raise ValueError(f'Not enough employees available for {shift} on Day {day}')

        selected = available.sample(n=demand)

        for _, row in selected.iterrows():
            daily_schedule.append({
                'day': day,
                'shift': shift,
                'employee_id': row['employee_id'],
                'hourly_wage': row['hourly_wage'],
                'scheduled_hours': row['scheduled_hours']
            })
            assigned_today.add(row['employee_id'])

    return daily_schedule

def create_random_chromosome(employee_df, config, dataset_size):
    '''
    Generates a full 7-day schedule plan.
    '''
    chromosome = []
    for day in range(1, 8):
        daily_schedule = create_daily_schedule(employee_df, config, day, dataset_size)
        chromosome.extend(daily_schedule)
    return chromosome

def initialize_population(employee_df, config, dataset_size):
    '''
    Builds the starting generation array.
    '''
    population = []
    for _ in range(config['population_size']):
        chromosome = create_random_chromosome(employee_df, config, dataset_size)
        population.append(chromosome)
    return population

def create_employee_lookup(employee_df):
    '''
    Creates a fast-access dictionary look-up for employee profiles.
    '''
    employee_lookup = {}
    for _, row in employee_df.iterrows():
        employee_lookup[row['employee_id']] = {
            'hourly_wage': row['hourly_wage'],
            'scheduled_hours': row['scheduled_hours'],
            'available_morning': row['available_morning'],
            'available_afternoon': row['available_afternoon'],
            'available_evening': row['available_evening']
        }
    return employee_lookup


# ==========================================
# 2. FITNESS EVALUATION & CONSTRAINTS
# ========================================== 

def calculate_labour_cost(chromosome):
    '''
    Calculates total fiscal operational cost.
    '''
    total_cost = 0
    for assignment in chromosome:
        total_cost += (assignment['hourly_wage'] * assignment['scheduled_hours'])
    return total_cost

def calculate_availability_penalty(chromosome, employee_lookup, config):
    '''
    Penalizes scheduling conflicts against an employee's requested availability.
    '''
    penalty = 0
    shift_columns = {
        'Morning': 'available_morning',
        'Afternoon': 'available_afternoon',
        'Evening': 'available_evening'
    }

    for assignment in chromosome:
        employee = employee_lookup[assignment['employee_id']]
        shift = assignment['shift']
        if employee[shift_columns[shift]] == 0:
            penalty += config['penalties']['unavailable']
    return penalty

def calculate_weekly_hours_penalty(chromosome, config):
    '''
    Applies penalties if working hours cross structural regulatory limits.
    '''
    penalty = 0
    employee_hours = {}

    for assignment in chromosome:
        emp_id = assignment['employee_id']
        employee_hours[emp_id] = employee_hours.get(emp_id, 0) + assignment['scheduled_hours']

    for hours in employee_hours.values():
        if hours > config['max_weekly_hours']:
            penalty += config['penalties']['weekly_hours']
    return penalty

def calculate_duplicate_penalty(chromosome, config):
    '''
    Penalizes double-booking shifts on identical working days.
    '''
    penalty = 0
    assignments = set()

    for assignment in chromosome:
        key = (assignment['employee_id'], assignment['day'])
        if key in assignments:
            penalty += config['penalties']['duplicate_shift']
        else:
            assignments.add(key)
    return penalty

def calculate_fitness(chromosome, employee_lookup, config):
    '''
    Consolidated objective cost function. Lower scores mean better optimization.
    '''
    labour_cost = calculate_labour_cost(chromosome)
    availability_penalty = calculate_availability_penalty(chromosome, employee_lookup, config)
    weekly_hours_penalty = calculate_weekly_hours_penalty(chromosome, config)
    duplicate_penalty = calculate_duplicate_penalty(chromosome, config)

    return labour_cost + availability_penalty + weekly_hours_penalty + duplicate_penalty


# ==========================================
# 3. GENETIC OPERATORS (EVOLUTION MECHANISMS)
# ========================================== 

def tournament_selection(population, employee_lookup, config):
    '''
    Selects parent candidate via mini-tournament pools.
    '''
    competitors = random.sample(population, config['tournament_size'])
    winner = min(competitors, key=lambda ch: calculate_fitness(ch, employee_lookup, config))
    return winner

def crossover(parent1, parent2, config):
    '''
    Day-Level Single-Point Crossover to keep chronological shifts intact.
    '''
    if random.random() > config['crossover_probability']:
        return copy.deepcopy(parent1), copy.deepcopy(parent2)

    # Organise structures by day unit rather than array index slices
    days_p1 = {d: [a for a in parent1 if a['day'] == d] for d in range(1, 8)}
    days_p2 = {d: [a for a in parent2 if a['day'] == d] for d in range(1, 8)}

    crossover_day = random.randint(2, 6)
    child1, child2 = [], []

    for day in range(1, 8):
        if day < crossover_day:
            child1.extend(days_p1[day])
            child2.extend(days_p2[day])
        else:
            child1.extend(days_p2[day])
            child2.extend(days_p1[day])

    return child1, child2

def mutate(chromosome, employee_df, config):
    '''
    Mutates a single shift allocation mapping inside a schedule chromosome.
    '''
    mutated = copy.deepcopy(chromosome)
    if random.random() > config['mutation_probability']:
        return mutated

    assignment_index = random.randint(0, len(mutated) - 1)
    assignment = mutated[assignment_index]
    shift = assignment['shift']

    # Find alternatives that match the required profile criteria
    available = employee_df[employee_df[f'available_{shift.lower()}'] == 1]
    available = available[available['employee_id'] != assignment['employee_id']]

    if len(available) == 0:
        return mutated

    new_employee = available.sample(1).iloc[0]
    
    # Update properties
    assignment['employee_id'] = new_employee['employee_id']
    assignment['hourly_wage'] = new_employee['hourly_wage']
    assignment['scheduled_hours'] = new_employee['scheduled_hours']

    return mutated

def evolve_population(population, employee_df, employee_lookup, config):
    '''
    Coordinates elitism strategies and processes offspring generations.
    '''
    new_population = []

    # Apply Elitism Strategy
    sorted_population = sorted(
        population, 
        key=lambda ch: calculate_fitness(ch, employee_lookup, config)
    )
    elite_size = config['elite_size']
    new_population.extend(copy.deepcopy(sorted_population[:elite_size]))

    # Generate Offspring for the remaining population pool slots
    while len(new_population) < config['population_size']:
        parent1 = tournament_selection(population, employee_lookup, config)
        parent2 = tournament_selection(population, employee_lookup, config)

        child1, child2 = crossover(parent1, parent2, config)

        child1 = mutate(child1, employee_df, config)
        child2 = mutate(child2, employee_df, config)

        new_population.append(child1)
        if len(new_population) < config['population_size']:
            new_population.append(child2)

    return new_population


# ==========================================
# 4. MAIN ENGINE EXECUTION RUNNER
# ========================================== 

def run_ga(employee_df, config, dataset_size):
    '''
    Main execution loop running the complete Genetic Algorithm over generations.
    '''
    start = time.time()

    print(f'Total Registered Employees : {len(employee_df)}')
    employee_lookup = create_employee_lookup(employee_df)

    # Step 1: Initialize starting generation population
    population = initialize_population(employee_df, config, dataset_size)
    print(f'Initial Population Baseline Created : {len(population)}')

    # Track initial performance
    best_initial = min(population, key=lambda ch: calculate_fitness(ch, employee_lookup, config))
    best_fitness_baseline = calculate_fitness(best_initial, employee_lookup, config)
    print(f'Generation 0 Best Fitness Baseline: {best_fitness_baseline:.2f}')

    # Step 2: Main Generational Iteration Loop
    fitness_history = [] 
    for generation in range(1, config['generations'] + 1):
        population = evolve_population(population, employee_df, employee_lookup, config)

        # Log out metrics status to capture optimization convergence
        if generation % 10 == 0 or generation == 1:
            current_best = min(population, key=lambda ch: calculate_fitness(ch, employee_lookup, config))
            score = calculate_fitness(current_best, employee_lookup, config)
            fitness_history.append(score)
            print(f'Generation {generation:03d} -> Best Fitness Value: {score:.2f}')   

    # Step 3: Extract optimal output individual profile results
    final_best_chromosome = min(population, key=lambda ch: calculate_fitness(ch, employee_lookup, config))    
    best_fitness = calculate_fitness(final_best_chromosome, employee_lookup, config)

    end = time.time()
    execution_time = end - start

    return {
        'schedule': final_best_chromosome,
        'fitness_history': fitness_history,
        'best_fitness': best_fitness,
        'execution_time' : execution_time
    }

    