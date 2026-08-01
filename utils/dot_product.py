
def dot_product(v1, v2):
    return sum(v1[i]*v2[i] for i in range(3))


def dot_product(a, b):
    return sum(map(operator.mul, a, b))

