
def test_both_ref_mutators():
    """Tests a complex chain of nested eigen/numpy references"""

    m.reset_refs()  # In case another test already changed it

    z = m.get_cm_ref()  # numpy -> eigen
    z[0, 2] -= 3
    z2 = m.incr_matrix(z, 1)  # numpy -> eigen -> numpy -> eigen
    z2[1, 1] += 6
    z3 = m.incr_matrix(z, 2)  # (numpy -> eigen)^3
    z3[2, 2] += -5
    z4 = m.incr_matrix(z, 3)  # (numpy -> eigen)^4
    z4[1, 1] -= 1
    z5 = m.incr_matrix(z, 4)  # (numpy -> eigen)^5
    z5[0, 0] = 0
    assert np.all(z == z2)
    assert np.all(z == z3)
    assert np.all(z == z4)
    assert np.all(z == z5)
    expect = np.array([[0.0, 22, 20], [31, 37, 33], [41, 42, 38]])
    assert np.all(z == expect)

    y = np.array(range(100), dtype="float64").reshape(10, 10)
    y2 = m.incr_matrix_any(y, 10)  # np -> eigen -> np
    y3 = m.incr_matrix_any(
        y2[0::2, 0::2], -33
    )  # np -> eigen -> np slice -> np -> eigen -> np
    y4 = m.even_rows(y3)  # numpy -> eigen slice -> (... y3)
    y5 = m.even_cols(y4)  # numpy -> eigen slice -> (... y4)
    y6 = m.incr_matrix_any(y5, 1000)  # numpy -> eigen -> (... y5)

    # Apply same mutations using just numpy:
    yexpect = np.array(range(100), dtype="float64").reshape(10, 10)
    yexpect += 10
    yexpect[0::2, 0::2] -= 33
    yexpect[0::4, 0::4] += 1000
    assert np.all(y6 == yexpect[0::4, 0::4])
    assert np.all(y5 == yexpect[0::4, 0::4])
    assert np.all(y4 == yexpect[0::4, 0::2])
    assert np.all(y3 == yexpect[0::2, 0::2])
    assert np.all(y2 == yexpect)
    assert np.all(y == yexpect)

