from pulp import *
import time


def run_mip(employee_df, config, dataset_size):
    '''
    Runs the Mixed Integer Programming workforce scheduler.
    '''
    start = time.time()

    print(f'Employees : {len(employee_df)}')

    # Create optimisation model
    model = LpProblem('Workforce_Scheduling', LpMinimize)

    # ----------------------------------
    # Sets
    # ----------------------------------

    employees = employee_df['employee_id'].tolist()
    days = range(1, 8)
    shifts = ['Morning', 'Afternoon', 'Evening']
    print('Model created.')

    # ----------------------------------
    # Decision Variables
    # ----------------------------------

    x = LpVariable.dicts('Assign', (employees, days, shifts), cat=LpBinary)

    print(f'Decision Variables Created : {len(employees) * len(days) * len(shifts)}')

    employee_lookup = create_employee_lookup(employee_df)
    model += pulp.lpSum(
        employee_lookup[e]['hourly_wage'] * employee_lookup[e]['scheduled_hours'] * x[e][d][s]
        for e in employees
        for d in days
        for s in shifts
    )
    print('Objective Function Added.')

    # ----------------------------------
    # Shift Demand Constraints
    # ----------------------------------

    # demand = config['shift_demand_24']
    shift_demand = config['shift_demand_24'] if dataset_size == 24 else config['shift_demand_65']

    for d in days:
        for s in shifts:
            model += (lpSum(x[e][d][s] for e in employees) == shift_demand[s])

    print('Shift Demand Constraints Added.')

    # ----------------------------------
    # Employee Availability Constraints
    # ----------------------------------

    shift_columns = {
        'Morning': 'available_morning',
        'Afternoon': 'available_afternoon',
        'Evening': 'available_evening'
    }

    for e in employees:
        for d in days:
            for s in shifts:
                model += (x[e][d][s] <= employee_lookup[e][shift_columns[s]] )

    print('Availability Constraints Added.')

    # ----------------------------------
    # One Shift Per Day Constraints
    # ----------------------------------

    for e in employees:
        for d in days:
            model += (lpSum(x[e][d][s] for s in shifts) <= 1)

    print('One Shift Per Day Constraints Added.')

    # ----------------------------------
    # Weekly Hours Constraints
    # ----------------------------------

    for e in employees:
        model += (lpSum(employee_lookup[e]['scheduled_hours'] * x[e][d][s]
                for d in days
                for s in shifts
            ) <= config['max_weekly_hours'])

    print('Weekly Hours Constraints Added.')

    # ----------------------------------
    # Solve Model
    # ----------------------------------

    print('Solving MIP Model...')

    model.solve(PULP_CBC_CMD(msg=True))
    print('Solver Status:', LpStatus[model.status])
    print('Optimal Labour Cost:', value(model.objective))

    schedule = extract_schedule(model, x,employees, days, shifts, employee_lookup)

    print(f'Assignments Created : {len(schedule)}')

    print('\nSample Schedule', schedule)

    
    for assignment in schedule[:10]:
        print(
            f"Day {assignment['day']} | "
            f"{assignment['shift']} | "
            f"Employee {assignment['employee_id']}"
        )
    
    end = time.time()
    execution_time = end - start

    return {
    'status': LpStatus[model.status],
    'objective': value(model.objective),
    'schedule': schedule,
    'execution_time' : execution_time
}

def extract_schedule(model, x, employees, days, shifts, employee_lookup):

    schedule = []

    for e in employees:
        for d in days:
            for s in shifts:
                if value(x[e][d][s]) == 1:
                    schedule.append({
                        'employee_id': e,
                        'day': d,
                        'shift': s,
                        'hourly_wage':
                            employee_lookup[e]['hourly_wage'],
                        'scheduled_hours':
                            employee_lookup[e]['scheduled_hours']
                    })

    return schedule

def create_employee_lookup(employee_df):

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