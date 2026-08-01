
def test_fromstring():
    o = 1 + LD_INFO.eps
    s = (" " + str(o)) * 5
    a = np.array([o] * 5)
    assert_equal(np.fromstring(s, sep=" ", dtype=np.longdouble), a,
                 err_msg=f"reading '{s}'")

