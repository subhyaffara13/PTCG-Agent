
def construct_c(num, den, x, poles, muls):
    """
    Helper function to calculate the coefficients
    in the c-vector for each pole.
    """
    c = []
    for pole, mul in zip(poles, muls):
        c.append([])

        # Case 3
        if mul == 1:
            # Add the coefficients from Case 3
            c[-1].extend(construct_c_case_3())

        # Case 1
        elif mul == 2:
            # Add the coefficients from Case 1
            c[-1].extend(construct_c_case_1(num, den, x, pole))

        # Case 2
        else:
            # Add the coefficients from Case 2
            c[-1].extend(construct_c_case_2(num, den, x, pole, mul))

    return c

