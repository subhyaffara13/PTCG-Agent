
def conic_coeff(variables, equation):
    if total_degree(equation) != 2:
        raise ValueError()
    x = variables[0]
    y = variables[1]

    equation = expand(equation)
    a = equation.coeff(x**2)
    b = equation.coeff(x*y)
    c = equation.coeff(y**2)
    d = equation.coeff(x, 1).coeff(y, 0)
    e = equation.coeff(y, 1).coeff(x, 0)
    f = equation.coeff(x, 0).coeff(y, 0)
    return a, b, c, d, e, f

