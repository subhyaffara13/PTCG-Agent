
def register_extension_dtype(cls: type_t[ExtensionDtypeT]) -> type_t[ExtensionDtypeT]:
    """
    Register an ExtensionType with pandas as class decorator.

    This enables operations like ``.astype(name)`` for the name
    of the ExtensionDtype.

    Returns
    -------
    callable
        A class decorator.

    See Also
    --------
    api.extensions.ExtensionDtype : The base class for creating custom pandas
        data types.
    Series : One-dimensional array with axis labels.
    DataFrame : Two-dimensional, size-mutable, potentially heterogeneous
        tabular data.

    Examples
    --------
    >>> from pandas.api.extensions import register_extension_dtype, ExtensionDtype
    >>> @register_extension_dtype
    ... class MyExtensionDtype(ExtensionDtype):
    ...     name = "myextension"
    """
    _registry.register(cls)
    return cls

