
def check_support(dist):
    a, b = dist.support()
    check_nans_and_edges(dist, 'support', None, a)
    check_nans_and_edges(dist, 'support', None, b)
    assert a.shape == dist._shape
    assert b.shape == dist._shape
    assert a.dtype == dist._dtype
    assert b.dtype == dist._dtype

