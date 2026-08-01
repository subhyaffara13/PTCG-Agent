
def deprecate_data():
    sympy_deprecation_warning(
        """
        The data attribute of TensorIndexType is deprecated. Use The
        replace_with_arrays() method instead.
        """,
        deprecated_since_version="1.4",
        active_deprecations_target="deprecated-tensorindextype-attrs",
        stacklevel=4,
    )

