
def test_x0_solves_problem_exactly(solver, xp, batch_A, batch_b):
    # See gh-19948
    dtype = xpx.default_dtype(xp)
    mat = xp.tile(xp.eye(2, dtype=dtype), (*batch_A, 1, 1))
    rhs = xp.tile(xp.asarray([-1., -1.], dtype=dtype), (*batch_b, 1))

    sol, info = solver(mat, rhs, x0=rhs)
    expected = xp.broadcast_to(rhs, (*np.broadcast_shapes(batch_A, batch_b), 2))
    xp_assert_close(sol, expected)
    assert info == 0

