
def mutable_mapping_update(
    self,
    data: Mapping[T, U] | Iterable[tuple[T, U]] = (),
    /,
    **kwargs: Any,
) -> None:
    if isinstance(data, Mapping):
        # Merge standard mapping with PyMapping_Items
        for key, value in data.items():
            self[key] = value
    # FIXME: Enabling the `elif`-branch below needs too many `VariableClass.call_obj_hasattr` changes.
    #   >>> class Foo:
    #   ...     def __init__(self):
    #   ...         self.keys = lambda: ['a', 'b', 'c']  # not required to be a method
    #   ...
    #   ...     def __getitem__(self, key):
    #   ...         return 0
    #   ...
    #   >>> dict(Foo())
    #   {'a': 0, 'b': 0, 'c': 0}
    #
    # > This is a rare case, so we comment it out for now.
    #
    # elif hasattr(data, "keys"):
    #     # Merge mapping-like object with PyMapping_Keys + PyObject_GetItem
    #     for key in data.keys():
    #         self[key] = data[key]
    else:
        if not isinstance(data, Iterable):
            raise TypeError(f"{type(data).__name__!r} object is not iterable")
        # Likely a sequence of pairs
        for key, value in data:
            self[key] = value

    if kwargs:
        for key, value in kwargs.items():
            self[key] = value

