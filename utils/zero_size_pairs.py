
def zero_size_pairs(width, height):
    """Creates a generator which yields pairs of sizes.

    For each pair of sizes at least one of the sizes will have a 0 in it.
    """
    sizes = ((width, height), (width, 0), (0, height), (0, 0))

    return ((a, b) for a in sizes for b in sizes if 0 in a or 0 in b)

