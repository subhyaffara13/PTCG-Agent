
def x0_4(n):  # skip name check
    assert_equal(n % 3, 0)
    x0 = np.array([-1, 1/2, -1] * (n//3))
    return x0

