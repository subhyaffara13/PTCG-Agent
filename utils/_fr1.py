
def _fr1(a):
    """fix rank > 0 --> rank-0"""
    if a.size == 1:
        a = a.reshape(())
    return a

