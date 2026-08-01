
def test_gh5584(solver_name, rs_interface):
    # gh-5584 reported that an underflow can cause sign checks in the algorithm
    # to fail. Check that this is resolved.
    solver = ((lambda f, a, b, **kwargs: root_scalar(f, bracket=(a, b)))
              if rs_interface else getattr(zeros, solver_name))

    def f(x):
        return 1e-200*x

    # Report failure when signs are the same
    with pytest.raises(ValueError, match='...must have different signs'):
        solver(f, -0.5, -0.4, full_output=True)

    # Solve successfully when signs are different
    res = solver(f, -0.5, 0.4, full_output=True)
    res = res if rs_interface else res[1]
    assert res.converged
    assert_allclose(res.root, 0, atol=1e-8)

    # Solve successfully when one side is negative zero
    res = solver(f, -0.5, float('-0.0'), full_output=True)
    res = res if rs_interface else res[1]
    assert res.converged
    assert_allclose(res.root, 0, atol=1e-8)

