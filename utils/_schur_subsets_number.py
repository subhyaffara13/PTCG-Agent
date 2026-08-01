
def _schur_subsets_number(n):

    if n is S.Infinity:
        raise ValueError("Input must be finite")
    if n <= 0:
        raise ValueError("n must be a non-zero positive integer.")
    elif n <= 3:
        min_k = 1
    else:
        min_k = math.ceil(math.log(2*n + 1, 3))

    return Integer(min_k)

