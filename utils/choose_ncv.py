
def choose_ncv(k):
    """
    Choose number of lanczos vectors based on target number
    of singular/eigen values and vectors to compute, k.
    """
    return max(2 * k + 1, 20)

