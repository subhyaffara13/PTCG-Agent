
def test_cva2_cv0_branches():
    res, resp = special.mathieu_cem([40, 129], [13, 14], [30, 45])
    assert_allclose(res, np.array([-0.3741211, 0.74441928]))
    assert_allclose(resp, np.array([-37.02872758, -86.13549877]))

    res, resp = special.mathieu_sem([40, 129], [13, 14], [30, 45])
    assert_allclose(res, np.array([0.92955551, 0.66771207]))
    assert_allclose(resp, np.array([-14.91073448, 96.02954185]))

