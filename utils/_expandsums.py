import itertools

def _expandsums(args: list[sympy.Expr]) -> tuple[sympy.Expr, bool]:
    """
    Expand products of sums into sums of products.

    This function takes a list of sympy expressions and separates them into
    additive expressions (those with is_Add=True) and other expressions.
    It then computes the distributive product, expanding (a+b)*(c+d) into a*c + a*d + b*c + b*d.

    Args:
        args: A list of sympy expressions to expand

    Returns:
        A tuple containing:
        - The expanded expression as a sympy.Expr
        - A boolean indicating whether expansion occurred (True if multiple additive
          expressions were present or if there was at least one additive and one other expression)
    """
    adds: list[sympy.Expr] = []
    other: list[sympy.Expr] = []
    for arg in args:
        if arg.is_Add:
            adds.append(arg)
        else:
            other.append(arg)

    result = [sympy.Mul(*other)]
    for add in adds:
        result = [a * b for a, b in itertools.product(result, add.args)]

    result = sympy.Add(*result)
    return result, len(adds) > 1 or (len(adds) > 0 and len(other) > 0)

