
def max_with_index(value, index, dim):
    return tl.reduce((value, index), dim, maximum_with_index)

