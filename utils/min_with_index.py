
def min_with_index(value, index, dim):
    return tl.reduce((value, index), dim, minimum_with_index)

