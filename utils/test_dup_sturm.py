
def test_dup_sturm():
    R, x = ring("x", QQ)

    assert R.dup_sturm(5) == [1]
    assert R.dup_sturm(x) == [x, 1]

    f = x**3 - 2*x**2 + 3*x - 5
    assert R.dup_sturm(f) == [f, 3*x**2 - 4*x + 3, -QQ(10,9)*x + QQ(13,3), -QQ(3303,100)]

