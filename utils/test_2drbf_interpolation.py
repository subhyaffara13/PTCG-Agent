
def test_2drbf_interpolation():
    for function in FUNCTIONS:
        check_2drbf1d_interpolation(function)
        check_2drbf2d_interpolation(function)
        check_2drbf3d_interpolation(function)

