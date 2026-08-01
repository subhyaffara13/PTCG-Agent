
def get_versions_of_S6_subgroup(name):
    vers = [name.get_perm_group()]
    if INCLUDE_SEARCH_REPS:
        vers.append(S6_randomized[name])
    return vers

