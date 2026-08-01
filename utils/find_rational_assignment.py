
def find_rational_assignment(constr, assignment, iter=20):
    eps = sympify(1)

    for _ in range(iter):
        assign = {key: val[0] + val[1]*eps for key, val in assignment.items()}
        try:
            for cons in constr:
                assert cons.subs(assign) == True
            return assign
        except AssertionError:
            eps = eps/2

    return None

