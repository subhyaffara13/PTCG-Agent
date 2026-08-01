
def sympy_reduce_product(x):
    if type(x) is list:
        value = sympy.Integer(1)
        for v in x:
            value = value * v
    else:
        value = x
    return value

