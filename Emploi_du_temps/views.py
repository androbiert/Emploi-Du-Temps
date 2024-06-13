from django.shortcuts import render
from collections import defaultdict
import re
from constraint import Problem, AllDifferentConstraint

def create_schedule():
    days_per_group = 5
    slots_per_day = 5
    num_groups = 3
    courses = ['AI,Dr Lekehali', 'DA/CI,Dr Djennadi', 'Reseaux,Dr Zenadji', 'Security,Dr Djebari',
               'Méthodes formelles,Dr Zedek', 'Recherche operationel,Dr Isaadi', 'Analyse numérique,Dr Alkama']
    lecture_courses = [course + '_Cour' for course in courses]
    td_courses = [course + '_TD' for course in courses]
    tp_courses = ['AI_TP,Pr Abbas,', 'Reseaux_TP,Pr Zaidi']
    free_values = ['FREE1', 'FREE2', 'FREE3', 'FREE4', 'FREE5', 'FREE6', 'FREE7', 'FREE8']
    all_courses = td_courses + free_values + tp_courses + lecture_courses + ['Entreprenariat,Pr Kaci_Cour']

    problem = Problem()
    for group in range(num_groups):
        for day in range(days_per_group):
            for slot in range(slots_per_day):
                var = (group, day, slot)
                problem.addVariable(var, all_courses)

    problem.addConstraint(lambda c: c.startswith('FREE'), ((0, 2, 3),))
    problem.addConstraint(lambda c: c.startswith('FREE'), ((0, 2, 4),))
    problem.addConstraint(lambda c: c.startswith('FREE'), ((1, 2, 3),))
    problem.addConstraint(lambda c: c.startswith('FREE'), ((1, 2, 4),))
    problem.addConstraint(lambda c: c.startswith('FREE'), ((2, 2, 3),))
    problem.addConstraint(lambda c: c.startswith('FREE'), ((2, 2, 4),))

    def td_all_different_constraint(*args):
        td_courses_in_slot = [val for val in args if '_TD' in val]
        return len(td_courses_in_slot) == len(set(td_courses_in_slot))

    def lecture_same_constraint(*args):
        lectures_in_slot = [val for val in args if '_Cour' in val]
        return len(set(lectures_in_slot)) <= 1

    for day in range(days_per_group):
        for slot in range(slots_per_day):
            vars_in_slot = [(group, day, slot) for group in range(num_groups)]
            problem.addConstraint(lecture_same_constraint, vars_in_slot)
            problem.addConstraint(td_all_different_constraint, vars_in_slot)

    for group in range(num_groups):
        group_constraints = [(group, day, slot) for slot in range(slots_per_day) for day in range(days_per_group)]
        problem.addConstraint(AllDifferentConstraint(), group_constraints)

    def max_three_successive_work_slots(*slots):
        count = 0
        for slot in slots:
            if not slot.startswith('FREE'):
                count += 1
                if count > 3:
                    return False
            else:
                count = 0
        return True

    for group in range(num_groups):
        for day in range(days_per_group):
            variables = [(group, day, slot) for slot in range(slots_per_day)]
            problem.addConstraint(max_three_successive_work_slots, variables)

    solution = problem.getSolution()
    return solution

def organize_schedule(solution):
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
    group_schedules = defaultdict(dict)

    if solution:
        for (group, day, slot), course in solution.items():
            day_name = days[day]
            slot_number = slot + 1
            if course.startswith('FREE'):
                course_name = 'FREE'
            else:
                course_name = course

            if group == 0:
                group_name = 'Group 1'
            elif group == 1:
                group_name = 'Group 2'
            elif group == 2:
                group_name = 'Group 3'
            else:
                group_name = f'Group {group + 1}'

            if day_name not in group_schedules[group_name]:
                group_schedules[group_name][day_name] = {}

            group_schedules[group_name][day_name][slot_number] = course_name

    return group_schedules

def find_teachers_less_than_3_days(group_schedules):
    teacher_days = defaultdict(set)
    teacher_pattern = re.compile(r'(Pr|Dr)\s+([A-Za-z]+)_')

    for group_name, schedules in group_schedules.items():
        for day_name, day_schedule in schedules.items():
            for slot_number, course_name in day_schedule.items():
                match = teacher_pattern.search(course_name)
                if match:
                    teacher = match.group(2)
                    teacher_days[teacher].add(day_name)

    teachers_less_than_3_days = {
        'count': 0,
        'list': []
    }

    for teacher, days in teacher_days.items():
        if len(days) < 3:
            teachers_less_than_3_days['count'] += 1
            teachers_less_than_3_days['list'].append(teacher)

    return teachers_less_than_3_days


def schedule_view(request):
    solution = create_schedule()
    group_schedules = organize_schedule(solution)

    # Define the order of days (Sunday to Saturday)
    days_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    # Initialize dictionaries for each group
    dict_grp_1 = {}
    dict_grp_2 = {}
    dict_grp_3 = {}

    # Sort schedules by day and assign to respective dictionaries
    for group_name, schedule in group_schedules.items():
        sorted_schedule = {day: schedule[day] for day in days_order if day in schedule}
        if group_name == 'Group 1':
            dict_grp_1 = sorted_schedule
        elif group_name == 'Group 2':
            dict_grp_2 = sorted_schedule
        elif group_name == 'Group 3':
            dict_grp_3 = sorted_schedule

    # Find teachers working less than 3 days
    teachers_less_than_3_days = find_teachers_less_than_3_days(group_schedules)

    context = {
        'dict_grp_1': dict_grp_1,
        'dict_grp_2': dict_grp_2,
        'dict_grp_3': dict_grp_3,
        'teachers_less_than_3_days': teachers_less_than_3_days,
    }

    return render(request, 'Emploi_du_temps/index.html', context)
