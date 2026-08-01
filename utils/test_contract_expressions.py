
def test_contract_expressions(string: str, optimize: OptimizeKind, use_blas: bool, out_spec: bool) -> None:
    views = build_views(string)
    shapes = [view.shape if hasattr(view, "shape") else () for view in views]
    expected = contract(string, *views, optimize=False, use_blas=False)

    expr = contract_expression(string, *shapes, optimize=optimize, use_blas=use_blas)

    if out_spec and ("->" in string) and (string[-2:] != "->"):
        (out,) = build_views(string.split("->")[1])
        expr(*views, out=out)
    else:
        out = expr(*views)

    assert np.allclose(out, expected)

    # check representations
    assert string in expr.__repr__()
    assert string in expr.__str__()

