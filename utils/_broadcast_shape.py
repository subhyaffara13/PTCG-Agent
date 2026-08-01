
def _broadcast_shape(*args):
    """Returns the shape of the arrays that would result from broadcasting the
    supplied arrays against each other.
    """
    # use the old-iterator because np.nditer does not handle size 0 arrays
    # consistently
    b = np.broadcast(*args[:64])
    # unfortunately, it cannot handle 64 or more arguments directly
    for pos in range(64, len(args), 63):
        # ironically, np.broadcast does not properly handle np.broadcast
        # objects (it treats them as scalars)
        # use broadcasting to avoid allocating the full array
        b = broadcast_to(0, b.shape)
        b = np.broadcast(b, *args[pos:(pos + 63)])
    return b.shape

