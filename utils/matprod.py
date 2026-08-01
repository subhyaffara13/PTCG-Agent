
def matprod(x, y):
    if not USE_NAIVE_MATH:
        return x@y
    if len(x.shape) == 1 and len(y.shape) == 1:
        return inprod(x, y)
    elif len(x.shape) == 1 and len(y.shape) == 2:
        return matprod12(x, y)
    elif len(x.shape) == 2 and len(y.shape) == 1:
        return matprod21(x, y)
    elif len(x.shape) == 2 and len(y.shape) == 2:
        return matprod22(x, y)
    else:
        raise ValueError(f'Invalid shapes for x and y: {x.shape} and {y.shape}')

