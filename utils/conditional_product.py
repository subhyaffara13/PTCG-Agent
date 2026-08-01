
def conditional_product(*args: int) -> int:
    return functools.reduce(operator.mul, [x for x in args if x])

