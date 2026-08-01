
def test_Indexed_coeff():
    N = Symbol('N', integer=True)
    len_y = N
    i = Idx('i', len_y-1)
    y = IndexedBase('y', shape=(len_y,))
    a = (1/y[i+1]*y[i]).coeff(y[i])
    b = (y[i]/y[i+1]).coeff(y[i])
    assert a == b

