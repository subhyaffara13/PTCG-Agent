
def test_correct_fp_eps():
    # check that relative step size is correct for FP size
    EPS = np.finfo(np.float64).eps
    relative_step = {"2-point": EPS**0.5,
                    "3-point": EPS**(1/3),
                     "cs": EPS**0.5}
    for method in ['2-point', '3-point', 'cs']:
        assert_allclose(
            _eps_for_method(np.float64, np.float64, method),
            relative_step[method])
        assert_allclose(
            _eps_for_method(np.complex128, np.complex128, method),
            relative_step[method]
        )

    # check another FP size
    EPS = np.finfo(np.float32).eps
    relative_step = {"2-point": EPS**0.5,
                    "3-point": EPS**(1/3),
                     "cs": EPS**0.5}

    for method in ['2-point', '3-point', 'cs']:
        assert_allclose(
            _eps_for_method(np.float64, np.float32, method),
            relative_step[method]
        )
        assert_allclose(
            _eps_for_method(np.float32, np.float64, method),
            relative_step[method]
        )
        assert_allclose(
            _eps_for_method(np.float32, np.float32, method),
            relative_step[method]
        )

