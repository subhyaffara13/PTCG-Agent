
def test_theano(string: str) -> None:
    np = pytest.importorskip("numpy")
    theano = pytest.importorskip("theano")

    views = build_views(string)
    ein = contract(string, *views, optimize=False, use_blas=False)
    shps = [v.shape for v in views]

    expr = contract_expression(string, *shps, optimize=True)

    opt = expr(*views, backend="theano")
    assert np.allclose(ein, opt)

    # test non-conversion mode
    theano_views = [backends.to_theano(view) for view in views]
    theano_opt = expr(*theano_views)
    assert isinstance(theano_opt, theano.tensor.TensorVariable)

