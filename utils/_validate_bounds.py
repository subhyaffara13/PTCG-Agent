
def _validate_bounds(
    trait: Int[t.Any, t.Any] | Float[t.Any, t.Any], obj: t.Any, value: t.Any
) -> t.Any:
    """
    Validate that a number to be applied to a trait is between bounds.

    If value is not between min_bound and max_bound, this raises a
    TraitError with an error message appropriate for this trait.
    """
    if trait.min is not None and value < trait.min:
        raise TraitError(
            f"The value of the '{trait.name}' trait of {class_of(obj)} instance should "
            f"not be less than {trait.min}, but a value of {value} was "
            "specified"
        )
    if trait.max is not None and value > trait.max:
        raise TraitError(
            f"The value of the '{trait.name}' trait of {class_of(obj)} instance should "
            f"not be greater than {trait.max}, but a value of {value} was "
            "specified"
        )
    return value


def _validate_bounds(bounds, x0, meth):
    """Check that bounds are valid."""

    msg = "An upper bound is less than the corresponding lower bound."
    if np.any(bounds.ub < bounds.lb):
        raise ValueError(msg)

    msg = "The number of bounds is not compatible with the length of `x0`."
    try:
        bounds.lb = np.broadcast_to(bounds.lb, x0.shape)
        bounds.ub = np.broadcast_to(bounds.ub, x0.shape)
    except Exception as e:
        raise ValueError(msg) from e

    return bounds


def _validate_bounds(
    l_bounds: "npt.ArrayLike", u_bounds: "npt.ArrayLike", d: int
) -> tuple[np.ndarray, np.ndarray]:
    """Bounds input validation.

    Parameters
    ----------
    l_bounds, u_bounds : array_like (d,)
        Lower and upper bounds.
    d : int
        Dimension to use for broadcasting.

    Returns
    -------
    l_bounds, u_bounds : array_like (d,)
        Lower and upper bounds.

    """
    try:
        lower = np.broadcast_to(l_bounds, d)
        upper = np.broadcast_to(u_bounds, d)
    except ValueError as exc:
        msg = ("'l_bounds' and 'u_bounds' must be broadcastable and respect"
               " the sample dimension")
        raise ValueError(msg) from exc

    if not np.all(lower < upper):
        raise ValueError("Bounds are not consistent 'l_bounds' < 'u_bounds'")

    return lower, upper

