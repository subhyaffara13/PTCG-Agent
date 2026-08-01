
def test_jax_jit_gradient() -> None:
    jax = pytest.importorskip("jax")
    key = jax.random.PRNGKey(42)

    eq = "ij,jk,kl->"
    shapes = (2, 3), (3, 4), (4, 2)
    views = [jax.random.uniform(key, s) for s in shapes]
    expr = contract_expression(eq, *shapes)
    x0 = expr(*views)

    jit_expr = jax.jit(expr)
    x1 = jit_expr(*views).item()
    assert x1 == pytest.approx(x0, rel=1e-5)

    # jax only takes gradient w.r.t first argument
    grad_expr = jax.jit(jax.grad(lambda views: expr(*views)))
    view_grads = grad_expr(views)
    assert all(v1.shape == v2.shape for v1, v2 in zip(views, view_grads))

    # taking a step along the gradient should reduce our 'loss'
    new_views = [v - 0.001 * dv for v, dv in zip(views, view_grads)]
    x2 = jit_expr(*new_views).item()
    assert x2 < x1

