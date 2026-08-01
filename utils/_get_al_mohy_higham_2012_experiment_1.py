
def _get_al_mohy_higham_2012_experiment_1():
    """
    Return the test matrix from Experiment (1) of [1]_.

    References
    ----------
    .. [1] Awad H. Al-Mohy and Nicholas J. Higham (2012)
           "Improved Inverse Scaling and Squaring Algorithms
           for the Matrix Logarithm."
           SIAM Journal on Scientific Computing, 34 (4). C152-C169.
           ISSN 1095-7197

    """
    A = np.array([
        [3.2346e-1, 3e4, 3e4, 3e4],
        [0, 3.0089e-1, 3e4, 3e4],
        [0, 0, 3.2210e-1, 3e4],
        [0, 0, 0, 3.0744e-1]], dtype=float)
    return A

