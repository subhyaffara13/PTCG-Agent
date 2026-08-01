
def is_lambda(lamb):
    LAMBDA = lambda: 0  # noqa: E731
    return isinstance(lamb, type(LAMBDA)) and lamb.__name__ == LAMBDA.__name__


def isLambda(v):
    LAMBDA = lambda: 0
    return isinstance(v, type(LAMBDA)) and v.__name__ == LAMBDA.__name__

