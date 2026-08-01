
def inner_product(a: IntTuple, b: IntTuple) -> int:
    if is_tuple(a) and is_tuple(b):  # tuple tuple
        if len(a) != len(b):
            raise AssertionError
        return sum(inner_product(x, y) for x, y in zip(a, b))
    else:  # "int" "int"
        if is_tuple(a) or is_tuple(b):
            raise AssertionError
        return a * b

