
def test_czt_math(impulse, m, w, a):
    # z-transform of an impulse is 1 everywhere
    xp_assert_close(czt(impulse[2:], m=m, w=w, a=a),
                    np.ones(m, dtype=np.complex128), rtol=1e-10)

    # z-transform of a delayed impulse is z**-1
    xp_assert_close(czt(impulse[1:], m=m, w=w, a=a),
                    czt_points(m=m, w=w, a=a)**-1, rtol=1e-10)

    # z-transform of a 2-delayed impulse is z**-2
    xp_assert_close(czt(impulse, m=m, w=w, a=a),
                    czt_points(m=m, w=w, a=a)**-2, rtol=1e-10)

