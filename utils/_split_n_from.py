
def _split_n_from(n, min_size_of_first_part):
    # splits j in two parts of which the first is at least
    # the second argument
    assert n >= min_size_of_first_part
    for p1 in range(min_size_of_first_part, n + 1):
        yield p1, n - p1

