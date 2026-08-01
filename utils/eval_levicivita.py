
def eval_levicivita(*args):
    """Evaluate Levi-Civita symbol."""
    n = len(args)
    return prod(
        prod(args[j] - args[i] for j in range(i + 1, n))
        / factorial(i) for i in range(n))

