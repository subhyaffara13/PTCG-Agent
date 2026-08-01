
def wrap_constraints(g):
    cons = []
    if g is not None:
        if not isinstance(g, tuple | list):
            g = (g,)
        else:
            pass
        for g in g:
            cons.append({'type': 'ineq',
                         'fun': g})
        cons = tuple(cons)
    else:
        cons = None
    return cons

