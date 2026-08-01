
def construct_d(num, den, x, val_inf):
    """
    Helper function to calculate the coefficients
    in the d-vector based on the valuation of the
    function at oo.
    """
    N = -val_inf//2
    # Multiplicity of oo as a pole
    mul = -val_inf if val_inf < 0 else 0
    ser = rational_laurent_series(num, den, x, oo, mul, 1)

    # Case 4
    if val_inf < 0:
        d = construct_d_case_4(ser, N)

    # Case 5
    elif val_inf == 0:
        d = construct_d_case_5(ser)

    # Case 6
    else:
        d = construct_d_case_6(num, den, x)

    return d

