
def nth_product(index, *args):
    """Equivalent to ``list(product(*args))[index]``.

    The products of *args* can be ordered lexicographically.
    :func:`nth_product` computes the product at sort position *index* without
    computing the previous products.

        >>> nth_product(8, range(2), range(2), range(2), range(2))
        (1, 0, 0, 0)

    ``IndexError`` will be raised if the given *index* is invalid.
    """
    pools = list(map(tuple, reversed(args)))
    ns = list(map(len, pools))

    c = reduce(mul, ns)

    if index < 0:
        index += c

    if not 0 <= index < c:
        raise IndexError

    result = []
    for pool, n in zip(pools, ns):
        result.append(pool[index % n])
        index //= n

    return tuple(reversed(result))

