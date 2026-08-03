import sys

def test_gh_22683():
    b = 777.68760986
    a = np.array([b] * 10000, dtype=object)
    refc_start = sys.getrefcount(b)
    np.choose(np.zeros(10000, dtype=int), [a], out=a)
    np.choose(np.zeros(10000, dtype=int), [a], out=a)
    refc_end = sys.getrefcount(b)
    assert refc_end - refc_start < 10

