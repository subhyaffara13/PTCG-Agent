
def test_object_arrays_backend(string: str) -> None:
    np = pytest.importorskip("numpy")
    views = build_views(string)
    ein = contract(string, *views, optimize=False, use_blas=False)
    assert ein.dtype != object

    shps = [v.shape for v in views]
    expr = contract_expression(string, *shps, optimize=True)

    obj_views = [view.astype(object) for view in views]

    # try raw contract
    obj_opt = contract(string, *obj_views, backend="object")
    assert obj_opt.dtype == object
    assert np.allclose(ein, obj_opt.astype(float))

    # test expression
    obj_opt = expr(*obj_views, backend="object")
    assert obj_opt.dtype == object
    assert np.allclose(ein, obj_opt.astype(float))

