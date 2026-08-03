from typing import Set

def test_theano_with_constants(constants: Set[int]) -> None:
    np = pytest.importorskip("numpy")
    theano = pytest.importorskip("theano")

    eq = "ij,jk,kl->li"
    shapes = (2, 3), (3, 4), (4, 5)
    (non_const,) = {0, 1, 2} - constants
    ops = [np.random.rand(*shp) if i in constants else shp for i, shp in enumerate(shapes)]
    var = np.random.rand(*shapes[non_const])
    res_exp = contract(eq, *(ops[i] if i in constants else var for i in range(3)))

    expr = contract_expression(eq, *ops, constants=constants)

    # check theano
    res_got = expr(var, backend="theano")
    assert all(array is None or infer_backend(array) == "theano" for array in expr._evaluated_constants["theano"])
    assert np.allclose(res_exp, res_got)

    # check can call with numpy still
    res_got2 = expr(var, backend="numpy")
    assert np.allclose(res_exp, res_got2)

    # check theano call returns theano still
    res_got3 = expr(backends.to_theano(var))
    assert isinstance(res_got3, theano.tensor.TensorVariable)

