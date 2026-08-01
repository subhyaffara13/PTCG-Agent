
def is_normal_transformation_ok(eq):
    A = transformation_to_normal(eq)
    X, Y, Z = A*Matrix([x, y, z])
    simplified = diop_simplify(eq.subs(zip((x, y, z), (X, Y, Z))))

    coeff = dict([reversed(t.as_independent(*[X, Y, Z])) for t in simplified.args])
    for term in [X*Y, Y*Z, X*Z]:
        if term in coeff.keys():
            return False

    return True

