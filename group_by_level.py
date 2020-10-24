from break_into_subgroups import break_into_subgroups


def group_by_level(group):
    initial_groups = {
        'javascript': [],
        'python': [],
        'c#': [],
    }

    final_groups = []

    for attendee in group:
        if attendee.first_lang == 'other':
            if initial_groups.get(attendee.other_lang, False):
                intitial_groups[attendee.other_lang].append(attendee)
            else:
                initial_groups[attendee.other_lang] = [attendee]
        else:
            initial_groups[attendee.first_lang].append(attendee)

    def assign_to_largest_group(attendee):
        largest_group = ''
        largest_group_size = 0
        for group in initial_groups:
            if len(initial_groups[group]) > largest_group_size:
                largest_group_size = len(initial_groups[group])
                largest_group = group
        initial_groups[largest_group].append(attendee)

    # Reassign 'other' groups with only one person
    def reassign_singles(lang):
        attendees = initial_groups[lang]
        if len(attendees) == 1:
            attendee = attendees[0]
            attempt = 1
            assigned = False
            while attempt <= 3 and not assigned:
                if attempt == 1:
                    next_lang = attendee.second_lang
                    if next_lang != 'other':
                        initial_groups[next_lang].append(attendee)
                        assigned = True
                elif attempt == 2:
                    next_lang = attendee.third_lang
                    if next_lang != 'other':
                        initial_groups[next_lang].append(attendee)
                        assigned = True
                elif attempt == 3:
                    attendee.can_pair = False
                    largest_group = ''
                    largest_group_size = 0
                    for group in initial_groups:
                        if len(initial_groups[group]) > largest_group_size:
                            largest_group_size = len(initial_groups[group])
                            largest_group = group
                    initial_groups[largest_group].append(attendee)
                    assigned = True
                if assigned:
                    initial_groups[lang] = []
                attempt += 1

    for group in initial_groups:
        if group != 'javascript' and group != 'python' and group != 'c#':
            reassign_singles(group)
    reassign_singles('c#')
    reassign_singles('python')
    reassign_singles('javascript')

    for group, attendees in initial_groups.items():
        if len(attendees) == 1:
            inadvertant_loners.append([attendees[0]])
            assign_to_largest_group(attendee)

    for group, attendees in initial_groups.items():
        grouped = break_into_subgroups(attendees)
        for group in grouped:
            final_groups.append(group)

    return final_groups
