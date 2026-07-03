def evaluate_schedule(result):

    schedule = result['schedule']

    employee_hours = {}
    total_cost = 0
    employees_used = set()
    total_assignments = len(schedule)

    for assignment in schedule:
        emp = assignment['employee_id']
        employees_used.add(emp)

        total_cost += (
            assignment['hourly_wage']
            * assignment['scheduled_hours']
        )

        employee_hours[emp] = (
            employee_hours.get(emp, 0)
            + assignment['scheduled_hours']
        )

    average_hours = (
        sum(employee_hours.values())
        / len(employee_hours)
    )

    maximum_hours = max(employee_hours.values())

    return {
        'Labour Cost': total_cost,
        'Employees Used': len(employees_used),
        'Assignments': total_assignments,
        'Average Weekly Hours': round(average_hours,2),
        'Maximum Weekly Hours': maximum_hours,
        'execution_time' : result['execution_time']
    }