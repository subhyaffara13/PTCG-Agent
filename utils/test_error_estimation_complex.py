
def test_error_estimation_complex(solver_class):
    h = 0.2
    solver = solver_class(lambda t, y: 1j * y, 0, [1j], 1, first_step=h)
    solver.step()
    err_norm = solver._estimate_error_norm(solver.K, h, scale=[1])
    assert np.isrealobj(err_norm)

