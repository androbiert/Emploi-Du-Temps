# Assuming the following are defined:
# courses: dictionary where keys are course names and values are either a list of teachers or a single teacher
# days: list of days
# time_slots: dictionary where keys are days and values are the number of time slots available in that day
from constraint import Problem

# Example data
courses = {
    "Math": ["Teacher1", "Teacher2"],
    "Science": "Teacher3",
    "History": ["Teacher4","Teacher5"]
}
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
time_slots = {
    "Monday": 5,
    "Tuesday": 3,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 5
}

# Initialize the problem and the variable list
problem = Problem()
pr = []

# Add variables and their domains
for course, teachers in courses.items():
    if isinstance(teachers, list):
        for teacher in teachers:
            variable_name = f"{course}_{teacher}"
            domain = [(day, slot) for day in days for slot in range(1,time_slots[day]+1)]
            problem.addVariable(variable_name, domain)
            pr.append({variable_name: domain})
    else:
        variable_name = course
        domain = [(day, slot) for day in days for slot in range(1,time_slots[day]+1)]
        problem.addVariable(variable_name, domain)
        pr.append({variable_name: domain})

# Print the problem variables and their domains
for item in pr:
    print(item)
