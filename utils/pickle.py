
def pickle(t, func):
    """expose :attr:`~Pickler.dispatch` table for user-created extensions"""
    Pickler.dispatch[t] = func
    return

