
def _warn_on_None_dynamic_shape_dimension():
    msg = (
        "Using None as a dynamic shape dimension is deprecated. "
        "Please use Dim.STATIC instead"
    )
    # TODO(avik): raise an error in the future
    log.warning(msg)

