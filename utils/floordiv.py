
def floordiv(a, b):
    return ops.floordiv(a, b)


def floordiv(g: jit_utils.GraphContext, self, other):
    return floor_divide(g, self, other)

