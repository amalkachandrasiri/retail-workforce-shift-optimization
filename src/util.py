import pandas as pd

def display_roster(schedule, path):

    day_names = {
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday',
        7: 'Sunday'
    }

    roster = []

    for day in range(1, 8):

        row = {'Day': day_names[day]}

        for shift in ['Morning', 'Afternoon', 'Evening']:

            employees = sorted([
                a['employee_id']
                for a in schedule
                if a['day'] == day and a['shift'] == shift
            ])

            row[shift] = ', '.join(
                f'E{emp}' for emp in employees
            )

        roster.append(row)

    roster_df = pd.DataFrame(roster)

    print('\nWeekly Workforce Roster\n')
    print(roster_df.to_string(index = False))

    roster_df.to_csv(path, index = False)

    return roster_df

def print_summary(title, metrics):

    print('\n')
    print('='*60)
    print(title)
    print('='*60)

    for key, value in metrics.items():
        print(f'{key:<25}: {value:.2f}')