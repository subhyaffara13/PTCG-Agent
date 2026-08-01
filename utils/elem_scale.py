
def elem_scale(a: IntTuple, b: IntTuple) -> IntTuple:
    if is_tuple(a):
        if is_tuple(b):  # tuple tuple
            if len(a) != len(b):
                raise AssertionError
            return tuple(elem_scale(x, y) for x, y in zip(a, b))
        else:  # tuple "int"
            raise AssertionError("Invalid combination: tuple with int")
    else:
        if is_tuple(b):  # "int" tuple
            return elem_scale(a, product(b))
        else:  # "int" "int"
            return a * b

