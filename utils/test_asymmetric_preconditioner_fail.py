
def test_asymmetric_preconditioner_fail(problem_func):
    """Non-symmetric (non-Hermitian) preconditioner M
       should raise ValueError when check=True."""
    A, b = problem_func()
    rng = np.random.RandomState(4321)
    if np.iscomplexobj(A):
        M = rng.rand(10, 10) + 1j * rng.rand(10, 10)
        M = M + M.T.conj()
        M[1, 2] = 1 + 2j
        M[2, 1] = 3 + 0j  # break Hermitian symmetry
    else:
        M = rng.rand(10, 10)
        M = M + M.T
        M[1, 2] = 1.0
        M[2, 1] = 2.0  # break symmetry
    with assert_raises(ValueError):
        xp, info = minres(A, b, M=M, check=True)

