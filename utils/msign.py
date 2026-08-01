
def msign(x):
    """Returns the sign of x, or 0 if x is masked."""  # numpydoc ignore=RT01
    return ma.filled(np.sign(x), 0)

