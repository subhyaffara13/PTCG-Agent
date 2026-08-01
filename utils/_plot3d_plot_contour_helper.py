
def _plot3d_plot_contour_helper(Series, *args, **kwargs):
    """plot3d and plot_contour are structurally identical. Let's reduce
    code repetition.
    """
    # NOTE: if this import would be at the top-module level, it would trigger
    # SymPy's optional-dependencies tests to fail.
    from sympy.vector import BaseScalar

    args = _plot_sympify(args)
    plot_expr = _check_arguments(args, 1, 2, **kwargs)

    free_x = set()
    free_y = set()
    _types = (Symbol, BaseScalar, Indexed, AppliedUndef)
    for p in plot_expr:
        free_x |= {p[1][0]} if isinstance(p[1][0], _types) else {Symbol(p[1][0])}
        free_y |= {p[2][0]} if isinstance(p[2][0], _types) else {Symbol(p[2][0])}
    x = free_x.pop() if free_x else Symbol("x")
    y = free_y.pop() if free_y else Symbol("y")
    kwargs.setdefault("xlabel", x)
    kwargs.setdefault("ylabel", y)
    kwargs.setdefault("zlabel", Function('f')(x, y))

    # if a polar discretization is requested and automatic labelling has ben
    # applied, hide the labels on the x-y axis.
    if kwargs.get("is_polar", False):
        if callable(kwargs["xlabel"]):
            kwargs["xlabel"] = ""
        if callable(kwargs["ylabel"]):
            kwargs["ylabel"] = ""

    labels = kwargs.pop("label", [])
    rendering_kw = kwargs.pop("rendering_kw", None)
    series = _create_series(Series, plot_expr, **kwargs)
    _set_labels(series, labels, rendering_kw)
    plots = plot_factory(*series, **kwargs)
    if kwargs.get("show", True):
        plots.show()
    return plots

