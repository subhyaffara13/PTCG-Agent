
def _unlabeled_trees(n):
    """Implements OEIS A000055 (number of unlabeled trees)."""

    value = 0
    for k in range(n + 1):
        value += _rooted_trees(k) * _rooted_trees(n - k)
    if n % 2 == 0:
        value -= _rooted_trees(n // 2)
    return _rooted_trees(n) - value // 2

