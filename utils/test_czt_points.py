
def test_czt_points():
    for N in (1, 2, 3, 8, 11, 100, 101, 10007):
        xp_assert_close(czt_points(N), np.exp(2j*np.pi*np.arange(N)/N),
                        rtol=1e-30)

    xp_assert_close(czt_points(7, w=1), np.ones(7, dtype=np.complex128), rtol=1e-30)
    xp_assert_close(czt_points(11, w=2.),
                    1/(2**np.arange(11, dtype=np.complex128)), rtol=1e-30)

    func = CZT(12, m=11, w=2., a=1)
    xp_assert_close(func.points(), 1/(2**np.arange(11)), rtol=1e-30)

