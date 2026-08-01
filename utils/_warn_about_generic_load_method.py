
def _warn_about_generic_load_method(method_name):  # pragma: NO COVER
    """Warns that a generic load method is being used.

    This is to discourage use of the generic load methods in favor of
    more specific methods. The generic methods are more likely to lead to
    security issues if the input is not validated.

    Args:
        method_name (str): The name of the method being used.
    """

    warnings.warn(_GENERIC_LOAD_METHOD_WARNING.format(method_name), DeprecationWarning)

