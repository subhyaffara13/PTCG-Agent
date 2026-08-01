
def top_down(rule, fns=basic_fns):
    """Apply a rule down a tree running it on the top nodes first."""
    return chain(rule, lambda expr: sall(top_down(rule, fns), fns)(expr))


def top_down(brule, fns=basic_fns):
    """ Apply a rule down a tree running it on the top nodes first """
    return chain(do_one(brule, identity),
                 lambda expr: sall(top_down(brule, fns), fns)(expr))

