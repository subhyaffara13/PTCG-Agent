
def test_jax_with_constants(constants: Set[int]) -> None:
    jax = pytest.importorskip("jax")
    key = jax.random.PRNGKey(42)

    eq = "ij,jk,kl->li"
    shapes = (2, 3), (3, 4), (4, 5)
    (non_const,) = {0, 1, 2} - constants
    ops = [jax.random.uniform(key, shp) if i in constants else shp for i, shp in enumerate(shapes)]
    var = jax.random.uniform(key, shapes[non_const])
    res_exp = contract(eq, *(ops[i] if i in constants else var for i in range(3)))

    expr = contract_expression(eq, *ops, constants=constants)

    # check jax
    res_got = expr(var, backend="jax")
    # check jax versions of constants exist
    assert all(array is None or infer_backend(array).startswith("jax") for array in expr._evaluated_constants["jax"])
    assert jax.numpy.sum(jax.numpy.abs(res_exp - res_got)) < 1e-8

