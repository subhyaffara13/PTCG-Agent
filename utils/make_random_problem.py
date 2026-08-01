
def make_random_problem(num_variables=2, num_constraints=2, sparsity=.1, rational=True,
                        disable_strict = False, disable_nonstrict=False, disable_equality=False):
    def rand(sparsity=sparsity):
        if random() < sparsity:
            return sympify(0)
        if rational:
            int1, int2 = [randprime(0, 50) for _ in range(2)]
            return Rational(int1, int2) * choice([-1, 1])
        else:
            return randint(1, 10) * choice([-1, 1])

    variables = symbols('x1:%s' % (num_variables + 1))
    constraints = []
    for _ in range(num_constraints):
        lhs, rhs = sum(rand() * x for x in variables), rand(sparsity=0) # sparsity=0  bc of bug with smtlib_code
        options = []
        if not disable_equality:
            options += [Eq(lhs, rhs)]
        if not disable_nonstrict:
            options += [lhs <= rhs, lhs >= rhs]
        if not disable_strict:
            options += [lhs < rhs, lhs > rhs]

        constraints.append(choice(options))

    return constraints

