
def test_positional_error(solver, xp, batch_A, batch_b):
    A, b, x0 = _setup_random_system(xp, batch_A, batch_b)
    with pytest.raises(TypeError):
        solver(A, b, x0, 1e-5)

