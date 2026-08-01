
def construct_c_case_2(num, den, x, pole, mul):
    # Generate the coefficients using the recurrence
    # relation mentioned in (5.14) in the thesis (Pg 80)

    # r_i = mul/2
    ri = mul//2

    # Find the Laurent series coefficients about the pole
    ser = rational_laurent_series(num, den, x, pole, mul, 6)

    # Start with an empty memo to store the coefficients
    # This is for the plus case
    cplus = [0 for i in range(ri)]

    # Base Case
    cplus[ri-1] = sqrt(ser[2*ri])

    # Iterate backwards to find all coefficients
    s = ri - 1
    sm = 0
    for s in range(ri-1, 0, -1):
        sm = 0
        for j in range(s+1, ri):
            sm += cplus[j-1]*cplus[ri+s-j-1]
        if s!= 1:
            cplus[s-1] = (ser[ri+s] - sm)/(2*cplus[ri-1])

    # Memo for the minus case
    cminus = [-x for x in cplus]

    # Find the 0th coefficient in the recurrence
    cplus[0] = (ser[ri+s] - sm - ri*cplus[ri-1])/(2*cplus[ri-1])
    cminus[0] = (ser[ri+s] - sm  - ri*cminus[ri-1])/(2*cminus[ri-1])

    # Add both the plus and minus cases' coefficients
    if cplus != cminus:
        return [cplus, cminus]
    return cplus

