
def expand_groups_in_paired_modules_list(paired_modules_list):
    """Expands module pair groups larger than two into groups of two modules."""
    new_list = []

    for group in paired_modules_list:
        if len(group) == 1:
            raise ValueError("Group must have at least two modules")
        elif len(group) == 2:
            new_list.append(group)
        elif len(group) > 2:
            new_list.extend([group[i], group[i + 1]] for i in range(len(group) - 1))

    return new_list

