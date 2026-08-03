from typing import Callable

def register_series_accessor(name: str) -> Callable[[TypeT], TypeT]:
    """
    Register a custom accessor on Series objects.

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
    This function allows you to register a custom-defined accessor class for Series.
    The requirements for the accessor class are as follows:

    * Must contain an init method that:

      * accepts a single Series object

      * raises an AttributeError if the Series object does not have correctly
        matching inputs for the accessor

    * Must contain a method for each access pattern.

      * The methods should be able to take any argument signature.

      * Accessible using the @property decorator if no additional arguments are
        needed.

    Examples
    --------
    An accessor that only accepts integers could
    have a class defined like this:

    >>> @pd.api.extensions.register_series_accessor("int_accessor")
    ... class IntAccessor:
    ...     def __init__(self, pandas_obj):
    ...         if not pandas_obj.dtype == "int64":
    ...             raise AttributeError("The series must contain integer data only")
    ...         self._obj = pandas_obj
    ...
    ...     def sum(self):
    ...         return self._obj.sum()
    >>> df = pd.Series([1, 2, "x"])
    >>> df.int_accessor
    Traceback (most recent call last):
    ...
    AttributeError: The series must contain integer data only.
    >>> df = pd.Series([1, 2, 3])
    >>> df.int_accessor.sum()
    6
    """
    from pandas import Series

    return _register_accessor(name, Series)

