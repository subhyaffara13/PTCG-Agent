
def _is_selfridge_prp(n):
    """Lucas compositeness test with the Selfridge parameters for n.

    Explanation
    ===========

    The Lucas compositeness test checks whether n is a prime number.
    The test can be run with arbitrary parameters ``P`` and ``Q``, which also change the performance of the test.
    So, which parameters are most effective for running the Lucas compositeness test?
    As an algorithm for determining ``P`` and ``Q``, Selfridge proposed method A [1]_ page 1401
    (Since two methods were proposed, referred to simply as A and B in the paper,
    we will refer to one of them as "method A").

    method A fixes ``P = 1``. Then, ``D`` defined by ``D = P**2 - 4Q`` is varied from 5, -7, 9, -11, 13, and so on,
    with the first ``D`` being ``jacobi(D, n) == -1``. Once ``D`` is determined,
    ``Q`` is determined to be ``(P**2 - D)//4``.

    References
    ==========

    .. [1] Robert Baillie, Samuel S. Wagstaff, Lucas Pseudoprimes,
           Math. Comp. Vol 35, Number 152 (1980), pp. 1391-1417,
           https://doi.org/10.1090%2FS0025-5718-1980-0583518-6
           http://mpqs.free.fr/LucasPseudoprimes.pdf

    """
    for D in range(5, 1_000_000, 2):
        if D & 2: # if D % 4 == 3
            D = -D
        j = jacobi(D, n)
        if j == -1:
            return _lucas_sequence(n, 1, (1-D) // 4, n + 1)[0] == 0
        if j == 0 and D % n:
            return False
        # When j == -1 is hard to find, suspect a square number
        if D == 13 and is_square(n):
            return False
    raise ValueError("appropriate value for D cannot be found in is_selfridge_prp()")

