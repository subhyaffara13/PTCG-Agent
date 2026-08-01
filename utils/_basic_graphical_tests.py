
def _basic_graphical_tests(deg_sequence):
    # Sort and perform some simple tests on the sequence
    deg_sequence = nx.utils.make_list_of_ints(deg_sequence)
    p = len(deg_sequence)
    num_degs = [0] * p
    dmax, dmin, dsum, n = 0, p, 0, 0
    for d in deg_sequence:
        # Reject if degree is negative or larger than the sequence length
        if d < 0 or d >= p:
            raise nx.NetworkXUnfeasible
        # Process only the non-zero integers
        elif d > 0:
            dmax, dmin, dsum, n = max(dmax, d), min(dmin, d), dsum + d, n + 1
            num_degs[d] += 1
    # Reject sequence if it has odd sum or is oversaturated
    if dsum % 2 or dsum > n * (n - 1):
        raise nx.NetworkXUnfeasible
    return dmax, dmin, dsum, n, num_degs

