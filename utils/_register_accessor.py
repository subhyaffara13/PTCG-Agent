
def _register_accessor(
    name: str, cls: type[NDFrame | Index]
) -> Callable[[TypeT], TypeT]:
    """
    Register a custom accessor on objects.

    Parameters
    ----------
    name : str
        Name under which the accessor should be registered. A warning is issued
        if this name conflicts with a preexisting attribute.

    Returns
    -------
    callable
        A class decorator.

    See Also
    --------
    register_dataframe_accessor : Register a custom accessor on DataFrame objects.
    register_series_accessor : Register a custom accessor on Series objects.
    register_index_accessor : Register a custom accessor on Index objects.

    Notes
    -----
    This function allows you to register a custom-defined accessor class
    for pandas objects (DataFrame, Series, or Index).
    The requirements for the accessor class are as follows:

    * Must contain an init method that:

      * accepts a single object

      * raises an AttributeError if the object does not have correctly
        matching inputs for the accessor

    * Must contain a method for each access pattern.

      * The methods should be able to take any argument signature.

      * Accessible using the @property decorator if no additional arguments are
        needed.

    """

    def decorator(accessor: TypeT) -> TypeT:
        if hasattr(cls, name):
            warnings.warn(
                f"registration of accessor {accessor!r} under name "
                f"{name!r} for type {cls!r} is overriding a preexisting "
                f"attribute with the same name.",
                UserWarning,
                stacklevel=find_stack_level(),
            )
        setattr(cls, name, Accessor(name, accessor))
        cls._accessors.add(name)
        return accessor

    return decorator

