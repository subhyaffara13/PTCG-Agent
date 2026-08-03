from typing import Callable

def _interpolate_scipy_wrapper(
    x: np.ndarray,
    y: np.ndarray,
    new_x: np.ndarray,
    method: str,
    fill_value=None,
    bounds_error: bool = False,
    order=None,
    **kwargs,
):
    """
    Passed off to scipy.interpolate.interp1d. method is scipy's kind.
    Returns an array interpolated at new_x.  Add any new methods to
    the list in _clean_interp_method.
    """
    extra = f"{method} interpolation requires SciPy."
    import_optional_dependency("scipy", extra=extra)
    from scipy import interpolate

    new_x = np.asarray(new_x)

    # ignores some kwargs that could be passed along.
    alt_methods: dict[str, Callable[..., np.ndarray]] = {
        "barycentric": interpolate.barycentric_interpolate,
        "krogh": interpolate.krogh_interpolate,
        "from_derivatives": _from_derivatives,
        "piecewise_polynomial": _from_derivatives,
        "cubicspline": _cubicspline_interpolate,
        "akima": _akima_interpolate,
        "pchip": interpolate.pchip_interpolate,
    }

    interp1d_methods = [
        "nearest",
        "zero",
        "slinear",
        "quadratic",
        "cubic",
        "polynomial",
    ]
    terp: Callable[..., np.ndarray] | None
    if method in interp1d_methods:
        if method == "polynomial":
            kind = order
        else:
            kind = method
        terp = interpolate.interp1d(
            x, y, kind=kind, fill_value=fill_value, bounds_error=bounds_error
        )
        new_y = terp(new_x)
    elif method == "spline":
        # GH #10633, #24014
        if isna(order) or (order <= 0):
            raise ValueError(
                f"order needs to be specified and greater than 0; got order: {order}"
            )
        terp = interpolate.UnivariateSpline(x, y, k=order, **kwargs)
        new_y = terp(new_x)
    else:
        # GH 7295: need to be able to write for some reason
        # in some circumstances: check all three
        if not x.flags.writeable:
            x = x.copy()
        if not y.flags.writeable:
            y = y.copy()
        if not new_x.flags.writeable:
            new_x = new_x.copy()
        terp = alt_methods.get(method, None)
        if terp is None:
            raise ValueError(f"Can not interpolate with method={method}.")

        # Make sure downcast is not in kwargs for alt methods
        kwargs.pop("downcast", None)
        new_y = terp(x, y, new_x, **kwargs)
    return new_y

