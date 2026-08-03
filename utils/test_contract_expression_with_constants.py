from typing import Any, List

def test_contract_expression_with_constants(string: str, constants: List[int]) -> None:
    views = build_views(string)
    expected = contract(string, *views, optimize=False, use_blas=False)

    shapes = [view.shape if hasattr(view, "shape") else () for view in views]

    expr_args: List[Any] = []
    ctrc_args = []
    for i, (shape, view) in enumerate(zip(shapes, views)):
        if i in constants:
            expr_args.append(view)
        else:
            expr_args.append(shape)
            ctrc_args.append(view)

    expr = contract_expression(string, *expr_args, constants=constants)
    out = expr(*ctrc_args)
    assert np.allclose(expected, out)

