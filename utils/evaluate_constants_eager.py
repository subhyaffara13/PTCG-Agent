
def evaluate_constants_eager(const_arrays, expr):
    """Convert constant arguments to tensorflow_eager arrays, and perform any
    possible constant contractions.
    """
    return expr(*[to_tensorflow(x) for x in const_arrays], backend="tensorflow", evaluate_constants=True)

