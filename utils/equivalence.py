
def equivalence(max_num_pow, dem_pow):
    # this function is made for checking the equivalence with 2F1 type of equation.
    # max_num_pow is the value of maximum power of x in numerator
    # and dem_pow is list of powers of different factor of form (a*x b).
    # reference from table 1 in paper - "Non-Liouvillian solutions for second order
    # linear ODEs" by L. Chan, E.S. Cheb-Terrab.
    # We can extend it for 1F1 and 0F1 type also.

    if max_num_pow == 2:
        if dem_pow in [[2, 2], [2, 2, 2]]:
            return "2F1"
    elif max_num_pow == 1:
        if dem_pow in [[1, 2, 2], [2, 2, 2], [1, 2], [2, 2]]:
            return "2F1"
    elif max_num_pow == 0:
        if dem_pow in [[1, 1, 2], [2, 2], [1, 2, 2], [1, 1], [2], [1, 2], [2, 2]]:
            return "2F1"

    return None

