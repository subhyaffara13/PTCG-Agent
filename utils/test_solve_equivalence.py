
def test_solve_equivalence():
    # For toeplitz matrices, solve_toeplitz() should be equivalent to solve().
    random = np.random.RandomState(1234)
    for n in (1, 2, 3, 10):
        c = random.randn(n)
        if random.rand() < 0.5:
            c = c + 1j * random.randn(n)
        r = random.randn(n)
        if random.rand() < 0.5:
            r = r + 1j * random.randn(n)
        y = random.randn(n)
        if random.rand() < 0.5:
            y = y + 1j * random.randn(n)

        # Check equivalence when both the column and row are provided.
        actual = solve_toeplitz((c,r), y)
        desired = solve(toeplitz(c, r=r), y)
        assert_allclose(actual, desired)

        # Check equivalence when the column is provided but not the row.
        actual = solve_toeplitz(c, b=y)
        desired = solve(toeplitz(c), y)
        assert_allclose(actual, desired)

