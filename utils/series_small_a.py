
def series_small_a():
    """Tylor series expansion of Phi(a, b, x) in a=0 up to order 5.
    """
    order = 5
    a, b, x, k = symbols("a b x k")
    A = []  # terms with a
    X = []  # terms with x
    B = []  # terms with b (polygammas)
    # Phi(a, b, x) = exp(x)/gamma(b) * sum(A[i] * X[i] * B[i])
    expression = Sum(x**k/factorial(k)/gamma(a*k+b), (k, 0, S.Infinity))
    expression = gamma(b)/sympy.exp(x) * expression

    # nth term of taylor series in a=0: a^n/n! * (d^n Phi(a, b, x)/da^n at a=0)
    for n in range(0, order+1):
        term = expression.diff(a, n).subs(a, 0).simplify().doit()
        # set the whole bracket involving polygammas to 1
        x_part = (term.subs(polygamma(0, b), 1)
                  .replace(polygamma, lambda *args: 0))
        # sign convention: x part always positive
        x_part *= (-1)**n

        A.append(a**n/factorial(n))
        X.append(horner(x_part))
        B.append(horner((term/x_part).simplify()))

    s = "Tylor series expansion of Phi(a, b, x) in a=0 up to order 5.\n"
    s += "Phi(a, b, x) = exp(x)/gamma(b) * sum(A[i] * X[i] * B[i], i=0..5)\n"
    for name, c in zip(['A', 'X', 'B'], [A, X, B]):
        for i in range(len(c)):
            s += f"\n{name}[{i}] = " + str(c[i])
    return s

