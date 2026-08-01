
def _logexpxmexpy(x, y):
    """ Compute the log of the difference of the exponentials of two arguments.

    Avoids over/underflow, but does not prevent loss of precision otherwise.
    """
    return xpx.apply_where(x != y, (x, y),
                           lambda x, y: special.logsumexp([x, y+np.pi*1j], axis=0),
                           fill_value=-np.inf)

