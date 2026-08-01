
def construct_d_case_5(ser):
    # List to store coefficients for plus case
    dplus = [0, 0]

    # d_0  = sqrt(a_0)
    dplus[0] = sqrt(ser[0])

    # d_(-1) = a_(-1)/(2*d_0)
    dplus[-1] = ser[-1]/(2*dplus[0])

    # Coefficients for the minus case are just the negative
    # of the coefficients for the positive case.
    dminus = [-x for x in dplus]

    if dplus != dminus:
        return [dplus, dminus]
    return dplus

