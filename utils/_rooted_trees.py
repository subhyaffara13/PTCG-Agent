
def _rooted_trees(n):
    """Implements OEIS A000081 (number of unlabeled rooted trees)."""

    if n < 2:
        return n
    value = 0
    for j in range(1, n):
        for d in range(1, n):
            if j % d == 0:
                value += d * _rooted_trees(d) * _rooted_trees(n - j)
    return value // (n - 1)

