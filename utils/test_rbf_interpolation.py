
def test_rbf_interpolation():
    for function in FUNCTIONS:
        check_rbf1d_interpolation(function)
        check_rbf2d_interpolation(function)
        check_rbf3d_interpolation(function)

