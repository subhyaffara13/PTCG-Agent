
def test_lp():
    r1 = y + 2*z <= 3
    r2 = -x - 3*z <= -2
    r3 = 2*x + y + 7*z <= 5
    constraints = [r1, r2, r3, x >= 0, y >= 0, z >= 0]
    objective = -x - y - 5 * z
    ans = optimum, argmax = lp(max, objective, constraints)
    assert ans == lpmax(objective, constraints)
    assert objective.subs(argmax) == optimum
    for constr in constraints:
        assert constr.subs(argmax) == True

    r1 = x - y + 2*z <= 3
    r2 = -x + 2*y - 3*z <= -2
    r3 = 2*x + y - 7*z <= -5
    constraints = [r1, r2, r3, x >= 0, y >= 0, z >= 0]
    objective = -x - y - 5*z
    ans = optimum, argmax = lp(max, objective, constraints)
    assert ans == lpmax(objective, constraints)
    assert objective.subs(argmax) == optimum
    for constr in constraints:
        assert constr.subs(argmax) == True

    r1 = x - y + 2*z <= -4
    r2 = -x + 2*y - 3*z <= 8
    r3 = 2*x + y - 7*z <= 10
    constraints = [r1, r2, r3, x >= 0, y >= 0, z >= 0]
    const = 2
    objective = -x-y-5*z+const # has constant term
    ans = optimum, argmax = lp(max, objective, constraints)
    assert ans == lpmax(objective, constraints)
    assert objective.subs(argmax) == optimum
    for constr in constraints:
        assert constr.subs(argmax) == True

    # Section 4 Problem 1 from
    # http://web.tecnico.ulisboa.pt/mcasquilho/acad/or/ftp/FergusonUCLA_LP.pdf
    # answer on page 55
    v = x1, x2, x3, x4 = symbols('x1 x2 x3 x4')
    r1 = x1 - x2 - 2*x3 - x4 <= 4
    r2 = 2*x1 + x3 -4*x4 <= 2
    r3 = -2*x1 + x2 + x4 <= 1
    objective, constraints = x1 - 2*x2 - 3*x3 - x4, [r1, r2, r3] + [
        i >= 0 for i in v]
    ans = optimum, argmax = lp(max, objective, constraints)
    assert ans == lpmax(objective, constraints)
    assert ans == (4, {x1: 7, x2: 0, x3: 0, x4: 3})

    # input contains Floats
    r1 = x - y + 2.0*z <= -4
    r2 = -x + 2*y - 3.0*z <= 8
    r3 = 2*x + y - 7*z <= 10
    constraints = [r1, r2, r3] + [i >= 0 for i in (x, y, z)]
    objective = -x-y-5*z
    optimum, argmax = lp(max, objective, constraints)
    assert objective.subs(argmax) == optimum
    for constr in constraints:
        assert constr.subs(argmax) == True

    # input contains non-float or non-Rational
    r1 = x - y + sqrt(2) * z <= -4
    r2 = -x + 2*y - 3*z <= 8
    r3 = 2*x + y - 7*z <= 10
    raises(TypeError, lambda: lp(max, -x-y-5*z, [r1, r2, r3]))

    r1 = x >= 0
    raises(UnboundedLPError, lambda: lp(max, x, [r1]))
    r2 = x <= -1
    raises(InfeasibleLPError, lambda: lp(max, x, [r1, r2]))

    # strict inequalities are not allowed
    r1 = x > 0
    raises(TypeError, lambda: lp(max, x, [r1]))

    # not equals not allowed
    r1 = Ne(x, 0)
    raises(TypeError, lambda: lp(max, x, [r1]))

    def make_random_problem(nvar=2, num_constraints=2, sparsity=.1):
        def rand():
            if random() < sparsity:
                return sympify(0)
            int1, int2 = [randprime(0, 200) for _ in range(2)]
            return Rational(int1, int2)*choice([-1, 1])
        variables = symbols('x1:%s' % (nvar + 1))
        constraints = [(sum(rand()*x for x in variables) <= rand())
                       for _ in range(num_constraints)]
        objective = sum(rand() * x for x in variables)
        return objective, constraints, variables

    # equality
    r1 = Eq(x, y)
    r2 = Eq(y, z)
    r3 = z <= 3
    constraints = [r1, r2, r3]
    objective = x
    ans = optimum, argmax = lp(max, objective, constraints)
    assert ans == lpmax(objective, constraints)
    assert objective.subs(argmax) == optimum
    for constr in constraints:
        assert constr.subs(argmax) == True

