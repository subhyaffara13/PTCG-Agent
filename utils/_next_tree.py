
def _next_tree(candidate):
    """One iteration of the Wright, Richmond, Odlyzko and McKay
    algorithm."""

    # valid representation of a free tree if:
    # there are at least two vertices at layer 1
    # (this is always the case because we start at the path graph)
    left, rest = _split_tree(candidate)

    # and the left subtree of the root
    # is less high than the tree with the left subtree removed
    left_height = max(left)
    rest_height = max(rest)
    valid = rest_height >= left_height

    if valid and rest_height == left_height:
        # and, if left and rest are of the same height,
        # if left does not encompass more vertices
        if len(left) > len(rest):
            valid = False
        # and, if they have the same number or vertices,
        # if left does not come after rest lexicographically
        elif len(left) == len(rest) and left > rest:
            valid = False

    if valid:
        return candidate
    else:
        # jump to the next valid free tree
        p = len(left)
        new_candidate = _next_rooted_tree(candidate, p)
        if candidate[p] > 2:
            new_left, new_rest = _split_tree(new_candidate)
            new_left_height = max(new_left)
            suffix = range(1, new_left_height + 2)
            new_candidate[-len(suffix) :] = suffix
        return new_candidate

