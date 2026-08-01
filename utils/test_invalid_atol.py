
def test_invalid_atol(solver, atol, xp, batch_A, batch_b):
    if solver == minres:
        pytest.skip("minres has no `atol` argument")
    A, b, x0 = _setup_random_system(xp, batch_A, batch_b)
    with pytest.raises(ValueError):
        solver(A, b, x0, atol=atol)

