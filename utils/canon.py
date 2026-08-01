
def canon(*rules, **kwargs):
    """ Strategy for canonicalization.

    Explanation
    ===========

    Apply each rule in a bottom_up fashion through the tree.
    Do each one in turn.
    Keep doing this until there is no change.
    """
    return exhaust(top_down(exhaust(do_one(*rules)), **kwargs))


def canon(*rules):
    """ Strategy for canonicalization

    Apply each branching rule in a top-down fashion through the tree.
    Multiplex through all branching rule traversals
    Keep doing this until there is no change.
    """
    return exhaust(multiplex(*map(top_down, rules)))

