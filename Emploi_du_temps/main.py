from constraint import Problem, AllDifferentConstraint

# Define the problem
problem = Problem()

# Define the days and time slots
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
time_slots = { 'Sunday': 5, 'Monday': 5, 'Tuesday': 3, 'Wednesday': 5, 'Thursday': 5 }

# Define courses and sessions
courses = {
    'Sécurité': ['Teacher1_lecture', 'Teacher1_td'],
    'Méthodes formelles': ['Teacher2_lecture', 'Teacher2_td'],
    'Analyse numérique': ['Teacher3_lecture', 'Teacher3_td'],
    'Entrepreneuriat': ['Teacher4_lecture', 'Teacher4_td'],
    'Recherche opérationnelle 2': ['Teacher5_lecture', 'Teacher5_td'],
    'Distributed Architecture & Intensive Computing': ['Teacher6_lecture', 'Teacher6_td'],
    'Réseaux 2': ['Teacher7_lecture', 'Teacher8_td', 'Teacher9_tp'],
    'Artificial Intelligence': ['Teacher11_lecture', 'Teacher12_td', 'Teacher13_tp']
}

# Define the variables and their domains
for course, sessions in courses.items():
    for session in sessions:
        problem.addVariable(f"{course}_{session}", [(day, slot) for day in days for slot in range(time_slots[day])])


# No more than 3 successive slots for any session type
def successive_slots_constraint(*args):
    days_slots = {}
    for day, slot in args:
        if day not in days_slots:
            days_slots[day] = []
        days_slots[day].append(slot)
    for slots in days_slots.values():
        slots.sort()
        for i in range(len(slots) - 3):
            if slots[i] + 1 == slots[i + 1] == slots[i + 2] - 1 == slots[i + 3] - 2:
                return False
    return True

# Same course not in the same slot
def same_course_constraint(course1, course2):
    return course1 != course2

# Different courses for the same group should have different slot allocations
def different_courses_constraint(*args):
    return len(set(args)) == len(args)

# Add constraints to the problem
for course1 in courses:
    for session1 in courses[course1]:
        for course2 in courses:
            for session2 in courses[course2]:
                if course1 != course2 or session1 != session2:
                    problem.addConstraint(same_course_constraint, (f"{course1}_{session1}", f"{course2}_{session2}"))

# Add successive slots constraint
for course, sessions in courses.items():
    problem.addConstraint(successive_slots_constraint, [f"{course}_{session}" for session in sessions])

# Add all-different constraint for different courses
all_course_vars = []
for course, sessions in courses.items():
    for session in sessions:
        all_course_vars.append(f"{course}_{session}")
problem.addConstraint(AllDifferentConstraint(), all_course_vars)



# Solve the problem
solution = problem.getSolutions()

# Print the solution
if solution:
    for session, slot in solution.items():
        print(f"{session} -> Day: {slot[0]}, Slot: {slot[1]}")
else:
    print("No solution found")
