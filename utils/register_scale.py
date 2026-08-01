
def register_scale(scale_class):
    """
    Register a new kind of scale.

    Parameters
    ----------
    scale_class : subclass of `ScaleBase`
        The scale to register.
    """
    _scale_mapping[scale_class.name] = scale_class

    # migration code to handle the *axis* parameter
    has_axis_parameter = "axis" in inspect.signature(scale_class).parameters
    _scale_has_axis_parameter[scale_class.name] = has_axis_parameter
    if has_axis_parameter:
        _api.warn_deprecated(
            "3.11",
            message=f"The scale {scale_class.__qualname__!r} uses an 'axis' parameter "
                    "in the constructors. This parameter is pending-deprecated since "
                    "matplotlib 3.11. It will be fully deprecated in 3.13 and removed "
                    "in 3.15. Starting with 3.11, 'register_scale()' accepts scales "
                    "without the *axis* parameter.",
            pending=True,
        )

