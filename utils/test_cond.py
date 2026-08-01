
def test_cond():
    mp.dps = 15
    A = matrix([[1.2969, 0.8648], [0.2161, 0.1441]])
    assert cond(A, lambda x: mnorm(x,1)) == mpf('327065209.73817754')
    assert cond(A, lambda x: mnorm(x,inf)) == mpf('327065209.73817754')
    assert cond(A, lambda x: mnorm(x,'F')) == mpf('249729266.80008656')

