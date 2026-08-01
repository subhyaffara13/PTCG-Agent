
def f_gaussian_exact(a, b, alphas, xp):
    # Exact only when `a` and `b` are one of:
    #   (-oo, oo), or
    #   (0, oo), or
    #   (-oo, 0)
    # `alphas` can be arbitrary.

    ndim = xp_size(a)
    double_infinite_count = 0
    semi_infinite_count = 0

    for i in range(ndim):
        if xp.isinf(a[i]) and xp.isinf(b[i]):   # doubly-infinite
            double_infinite_count += 1
        elif xp.isinf(a[i]) != xp.isinf(b[i]):  # exclusive or, so semi-infinite
            semi_infinite_count += 1

    return (math.sqrt(math.pi) ** ndim) / (
        2**semi_infinite_count * xp.prod(alphas, axis=-1)
    )

