
def test_milp_1():
    # solve magic square problem
    n = 3
    A, b, c, numbers, M = magic_square(n)
    A = sparse.csc_array(A)  # confirm that sparse arrays are accepted
    res = milp(c=c*0, constraints=(A, b, b), bounds=(0, 1), integrality=1)

    # check that solution is a magic square
    x = np.round(res.x)
    s = (numbers.flatten() * x).reshape(n**2, n, n)
    square = np.sum(s, axis=0)
    np.testing.assert_allclose(square.sum(axis=0), M)
    np.testing.assert_allclose(square.sum(axis=1), M)
    np.testing.assert_allclose(np.diag(square).sum(), M)
    np.testing.assert_allclose(np.diag(square[:, ::-1]).sum(), M)

