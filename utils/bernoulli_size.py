
def bernoulli_size(n):
    """Accurately estimate the size of B_n (even n > 2 only)"""
    lgn = math.log(n,2)
    return int(2.326 + 0.5*lgn + n*(lgn - 4.094))

