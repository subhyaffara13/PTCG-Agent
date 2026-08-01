
def fill_(x, fill_value):
    return mutate_to(x, full_like(x, fill_value))


def fill_(a: TensorLikeType, value: NumberType) -> TensorLikeType:
    r = prims.fill(a, value)
    prims.copy_to(a, r)
    return a

