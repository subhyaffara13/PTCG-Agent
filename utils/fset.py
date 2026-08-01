
def fset(list_of_sets):
    """allows == to be used for list of sets"""
    return set(map(frozenset, list_of_sets))

