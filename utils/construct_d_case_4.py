
def construct_d_case_4(ser, N):
    # Initialize an empty vector
    dplus = [0 for i in range(N+2)]
    # d_N = sqrt(a_{2*N})
    dplus[N] = sqrt(ser[2*N])

    # Use the recurrence relations to find
    # the value of d_s
    for s in range(N-1, -2, -1):
        sm = 0
        for j in range(s+1, N):
            sm += dplus[j]*dplus[N+s-j]
        if s != -1:
            dplus[s] = (ser[N+s] - sm)/(2*dplus[N])

    # Coefficients for the case of d_N = -sqrt(a_{2*N})
    dminus = [-x for x in dplus]

    # The third equation in Eq 5.15 of the thesis is WRONG!
    # d_N must be replaced with N*d_N in that equation.
    dplus[-1] = (ser[N+s] - N*dplus[N] - sm)/(2*dplus[N])
    dminus[-1] = (ser[N+s] - N*dminus[N] - sm)/(2*dminus[N])

    if dplus != dminus:
        return [dplus, dminus]
    return dplus

