
def test_obj_func_returns_scalar():
    match = ("The user-provided "
             "objective function must "
             "return a scalar value.")
    with assert_raises(ValueError, match=match):
        optimize.minimize(lambda x: x, np.array([1, 1]), method='BFGS')

