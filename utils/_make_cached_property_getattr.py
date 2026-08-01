
def _make_cached_property_getattr(cached_properties, original_getattr, cls):
    lines = [
        # Wrapped to get `__class__` into closure cell for super()
        # (It will be replaced with the newly constructed class after construction).
        "def wrapper(_cls):",
        "    __class__ = _cls",
        "    def __getattr__(self, item, cached_properties=cached_properties, original_getattr=original_getattr, _cached_setattr_get=_cached_setattr_get):",
        "         func = cached_properties.get(item)",
        "         if func is not None:",
        "              result = func(self)",
        "              _setter = _cached_setattr_get(self)",
        "              _setter(item, result)",
        "              return result",
    ]
    if original_getattr is not None:
        lines.append(
            "         return original_getattr(self, item)",
        )
    else:
        lines.extend(
            [
                "         try:",
                "             return super().__getattribute__(item)",
                "         except AttributeError:",
                "             if not hasattr(super(), '__getattr__'):",
                "                 raise",
                "             return super().__getattr__(item)",
                "         original_error = f\"'{self.__class__.__name__}' object has no attribute '{item}'\"",
                "         raise AttributeError(original_error)",
            ]
        )

    lines.extend(
        [
            "    return __getattr__",
            "__getattr__ = wrapper(_cls)",
        ]
    )

    unique_filename = _generate_unique_filename(cls, "getattr")

    glob = {
        "cached_properties": cached_properties,
        "_cached_setattr_get": _OBJ_SETATTR.__get__,
        "original_getattr": original_getattr,
    }

    return _linecache_and_compile(
        "\n".join(lines), unique_filename, glob, locals={"_cls": cls}
    )["__getattr__"]

