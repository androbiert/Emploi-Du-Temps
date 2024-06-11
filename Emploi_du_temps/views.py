# from constraint import Problem, AllDifferentConstraint
# from django.shortcuts import render
# import logging
# import random
# def check_succession(solution):
#     day_sessions = {}
#     for session, (day, slot) in solution.items():
#         day_sessions.setdefault(day, []).append(session)

#     for day, sessions in day_sessions.items():
#         if len(sessions) > 1:
#             sorted_sessions = sorted(sessions, key=lambda session: solution[session][1])
#             for i in range(len(sorted_sessions) - 1):
#                 current_session = sorted_sessions[i]
#                 next_session = sorted_sessions[i + 1]
#                 if solution[current_session][1] == solution[next_session][1] - 1:
#                     return False
#     return True

# def has_conflicts(current_solution):
#     for variable, value in current_solution.items():
#         for var, val in current_solution.items():
#             if variable != var and value == val:
#                 return True
#     return False
# def backtrack(problem, current_solution, all_solutions):
#     if not problem:  # Termination condition: if the problem is empty
#         # Check if the current solution satisfies the succession constraint
#         if check_succession(current_solution):
#             all_solutions.append(current_solution.copy())
#         return
#     print(problem)
#     # Choose a variable from the problem dictionary
#     variable = next(iter(problem))
#     domain = problem[variable]

#     # Iterate over the domain of the chosen variable
#     for value in domain:
#         current_solution[variable] = value

#         # Create a reduced problem by removing the chosen variable
#         reduced_problem = {key: val for key, val in problem.items() if key != variable}

#         # Check if there are any conflicts in the reduced problem
#         if not has_conflicts(current_solution):
#             # Recursive call to solve the reduced problem
#             backtrack(reduced_problem, current_solution, all_solutions)

#         # Backtrack: remove the variable from the current solution
#         current_solution.pop(variable)

# def home(request):
#     # Define the problem
#     problem = {}

#     # Define the days and time slots
#     days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
#     time_slots = {'Sunday': 5, 'Monday': 5, 'Tuesday': 3, 'Wednesday': 5, 'Thursday': 5}

#     # Define the courses and teachers
#     courses = [
#         ('Sécurité', ['Teacher1_lecture', 'Teacher1_td']),
#         ('Méthodes formelles', ['Teacher2_lecture', 'Teacher2_td']),
#         ('Analyse numérique', ['Teacher3_lecture', 'Teacher3_td']),
#         ('Entrepreneuriat', ['Teacher4_lecture']),
#         ('Recherche opérationnelle 2', ['Teacher5_lecture', 'Teacher5_td']),
#         ('Distributed Architecture & Intensive Computing', ['Teacher6_lecture', 'Teacher6_td']),
#         ('Réseaux 2', ['Teacher7_lecture', 'Teacher8_td', 'Teacher9_tp']),
#         ('Artificial Intelligence', ['Teacher11_lecture', 'Teacher12_td', 'Teacher13_tp'])
#     ]

#     # Shuffle the courses
#     random.shuffle(courses)

#     # Define the variables and their domains
#     for course, sessions in courses:
#         for session in sessions:
#             problem[f"{course}_{session}"] = [(day, slot) for day in days for slot in range(time_slots[day])]

#     # Backtrack to find all solutions
#     all_solutions = []
#     backtrack(problem, {}, all_solutions)

#     # Choose a random valid solution
#     if all_solutions:
#         solution = random.choice(all_solutions)
#     else:
#         solution = None

#     # Prepare data for HTML
#     timetable = {day: ['Empty' for _ in range(time_slots[day])] for day in days}

#     if solution:
#         for session, (day, slot) in solution.items():
#             course, _ = session.rsplit('_', 1)
#             timetable[day][slot] = course

#     context = {'timetable': timetable}
#     return render(request, 'Emploi_du_temps/index.html', context)



from constraint import Problem, AllDifferentConstraint
from django.shortcuts import render
import random

def home(request):
    # Define the problem
    problem = Problem()

    # Define the days and time slots
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
    time_slots = { 'Sunday': 5, 'Monday': 5, 'Tuesday': 3, 'Wednesday': 5, 'Thursday': 5 }

    # Define the courses and teachers
    courses = [
        ('Sécurité', ['Teacher1_lecture', 'Teacher1_td']),
        ('Méthodes formelles', ['Teacher2_lecture', 'Teacher2_td']),
        ('Analyse numérique', ['Teacher3_lecture', 'Teacher3_td']),
        ('Entrepreneuriat', ['Teacher4_lecture']),
        ('Recherche opérationnelle 2', ['Teacher5_lecture', 'Teacher5_td']),
        ('Distributed Architecture & Intensive Computing', ['Teacher6_lecture', 'Teacher6_td']),
        ('Réseaux 2', ['Teacher7_lecture', 'Teacher8_td', 'Teacher9_tp']),
        ('Artificial Intelligence', ['Teacher11_lecture', 'Teacher12_td', 'Teacher13_tp'])
    ]

    # Shuffle the courses
    random.shuffle(courses)
    random.shuffle(x=[1,2,3,4])
    

    # Define the variables and their domains
    for course, sessions in courses:
        for session in sessions:
            # Add a variable for each session
            problem.addVariable(session, [(day, slot) for day in days for slot in range(time_slots[day])])

    # Ensure all sessions of the same course do not overlap
    all_sessions = [session for _, sessions in courses for session in sessions]
    problem.addConstraint(AllDifferentConstraint(), all_sessions)

    # Solve the problem to get the first solution
    solution = problem.getSolution()

    # If a solution is found, add it to a list of solutions
    solutions = [solution] if solution else []

    # Try to find additional solutions
    while True:
        # Try to find another solution
        solution = problem.getSolution()
        if solution:
            solutions.append(solution)
        else:
            break  # If no more solutions can be found, stop

    # Randomly select one solution from the list of solutions
    selected_solution = random.choice(solutions) if solutions else None

    # Prepare data for HTML
    timetable = {day: ['Empty' for _ in range(time_slots[day])] for day in days}

    if selected_solution:
        for session, (day, slot) in selected_solution.items():
            timetable[day][slot] = session

    context = {'timetable': timetable}
    return render(request, 'Emploi_du_temps/index.html', context)
