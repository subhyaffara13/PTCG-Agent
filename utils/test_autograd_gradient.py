
def test_autograd_gradient() -> None:
    np = pytest.importorskip("numpy")
    autograd = pytest.importorskip("autograd")

    eq = "ij,jk,kl->"
    shapes = (2, 3), (3, 4), (4, 2)
    views = [np.random.randn(*s) for s in shapes]
    expr = contract_expression(eq, *shapes)
    x0 = expr(*views)

    # autograd only takes gradient w.r.t first argument
    grad_expr = autograd.grad(lambda views: expr(*views))
    view_grads = grad_expr(views)
    assert all(v1.shape == v2.shape for v1, v2 in zip(views, view_grads))

    # taking a step along the gradient should reduce our 'loss'
    new_views = [v - 0.001 * dv for v, dv in zip(views, view_grads)]
    x1 = expr(*new_views)
    assert x1 < x0

