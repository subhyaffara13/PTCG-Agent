
def _check_shape(argshape, size):
    """
    This is a utility function used by `_rvs()` in the class geninvgauss_gen.
    It compares the tuple argshape to the tuple size.

    Parameters
    ----------
    argshape : tuple of integers
        Shape of the arguments.
    size : tuple of integers or integer
        Size argument of rvs().

    Returns
    -------
    The function returns two tuples, scalar_shape and bc.

    scalar_shape : tuple
        Shape to which the 1-d array of random variates returned by
        _rvs_scalar() is converted when it is copied into the
        output array of _rvs().

    bc : tuple of booleans
        bc is a tuple the same length as size. bc[j] is True if the data
        associated with that index is generated in one call of _rvs_scalar().

    """
    scalar_shape = []
    bc = []
    for argdim, sizedim in zip_longest(argshape[::-1], size[::-1],
                                       fillvalue=1):
        if sizedim > argdim or (argdim == sizedim == 1):
            scalar_shape.append(sizedim)
            bc.append(True)
        else:
            bc.append(False)
    return tuple(scalar_shape[::-1]), tuple(bc[::-1])


def _check_shape(name: str, shape: Shape, *param_shapes) -> None:
  if param_shapes:
    shape_ = lax.broadcast_shapes(shape, *param_shapes)  # pyrefly: ignore[no-matching-overload]
    if shape != shape_:
      msg = ("{} parameter shapes must be broadcast-compatible with shape "
             "argument, and the result of broadcasting the shapes must equal "
             "the shape argument, but got result {} for shape argument {}.")
      raise ValueError(msg.format(name, shape_, shape))

