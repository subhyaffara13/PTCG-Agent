
def _parse_eq_to_pure_multiplication(a_term, shape_a, b_term, shape_b, out):
    """If there are no contracted indices, then we can directly transpose and
    insert singleton dimensions into ``a`` and ``b`` such that (broadcast)
    elementwise multiplication performs the einsum.

    No need to cache this as it is within the cached
    ``_parse_eq_to_batch_matmul``.

    """
    desired_a = ""
    desired_b = ""
    new_shape_a = []
    new_shape_b = []
    for ix in out:
        if ix in a_term:
            desired_a += ix
            new_shape_a.append(shape_a[a_term.index(ix)])
        else:
            new_shape_a.append(1)
        if ix in b_term:
            desired_b += ix
            new_shape_b.append(shape_b[b_term.index(ix)])
        else:
            new_shape_b.append(1)

    if desired_a != a_term:
        eq_a = f"{a_term}->{desired_a}"
    else:
        eq_a = None
    if desired_b != b_term:
        eq_b = f"{b_term}->{desired_b}"
    else:
        eq_b = None

    return (
        eq_a,
        eq_b,
        new_shape_a,
        new_shape_b,
        None,  # new_shape_ab, not needed since not fusing
        None,  # perm_ab, not needed as we transpose a and b first
        True,  # pure_multiplication=True
    )

