
def _inherit_from_data(
    name: str, delegate: type, cache: bool = False, wrap: bool = False
):
    """
    Make an alias for a method of the underlying ExtensionArray.

    Parameters
    ----------
    name : str
        Name of an attribute the class should inherit from its EA parent.
    delegate : class
    cache : bool, default False
        Whether to convert wrapped properties into cache_readonly
    wrap : bool, default False
        Whether to wrap the inherited result in an Index.

    Returns
    -------
    attribute, method, property, or cache_readonly
    """
    attr = getattr(delegate, name)

    if isinstance(attr, property) or type(attr).__name__ == "getset_descriptor":
        # getset_descriptor i.e. property defined in cython class
        if cache:

            def cached(self):
                return getattr(self._data, name)

            cached.__name__ = name
            cached.__doc__ = attr.__doc__
            method = cache_readonly(cached)

        else:

            def fget(self):
                result = getattr(self._data, name)
                if wrap:
                    if isinstance(result, type(self._data)):
                        return type(self)._simple_new(result, name=self.name)
                    elif isinstance(result, ABCDataFrame):
                        return result.set_index(self)
                    return Index(result, name=self.name, dtype=result.dtype, copy=False)
                return result

            def fset(self, value) -> None:
                setattr(self._data, name, value)

            fget.__name__ = name
            fget.__doc__ = attr.__doc__

            method = property(fget, fset)

    elif not callable(attr):
        # just a normal attribute, no wrapping
        method = attr

    else:
        # error: Incompatible redefinition (redefinition with type "Callable[[Any,
        # VarArg(Any), KwArg(Any)], Any]", original type "property")
        def method(self, *args, **kwargs):  # type: ignore[misc]
            if "inplace" in kwargs:
                raise ValueError(f"cannot use inplace with {type(self).__name__}")
            result = attr(self._data, *args, **kwargs)
            if wrap:
                if isinstance(result, type(self._data)):
                    return type(self)._simple_new(result, name=self.name)
                elif isinstance(result, ABCDataFrame):
                    return result.set_index(self)
                return Index(result, name=self.name, dtype=result.dtype, copy=False)
            return result

        # error: "property" has no attribute "__name__"
        method.__name__ = name  # type: ignore[attr-defined]
        method.__doc__ = attr.__doc__
        method.__signature__ = signature(attr)  # type: ignore[attr-defined]
    return method

