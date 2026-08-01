
def _autoconvertible_to_cdata(tp: Type, api: mypy.plugin.CheckerPluginInterface) -> Type:
    """Get a type that is compatible with all types that can be implicitly converted to the given
    CData type.

    Examples:
    * c_int -> Union[c_int, int]
    * c_char_p -> Union[c_char_p, bytes, int, NoneType]
    * MyStructure -> MyStructure
    """
    allowed_types = []
    # If tp is a union, we allow all types that are convertible to at least one of the union
    # items. This is not quite correct - strictly speaking, only types convertible to *all* of the
    # union items should be allowed. This may be worth changing in the future, but the more
    # correct algorithm could be too strict to be useful.
    for t in flatten_nested_unions([tp]):
        t = get_proper_type(t)
        # Every type can be converted from itself (obviously).
        allowed_types.append(t)
        if isinstance(t, Instance):
            unboxed = _find_simplecdata_base_arg(t, api)
            if unboxed is not None:
                # If _SimpleCData appears in tp's (direct or indirect) bases, its type argument
                # specifies the type's "unboxed" version, which can always be converted back to
                # the original "boxed" type.
                allowed_types.append(unboxed)

                if t.type.has_base("ctypes._PointerLike"):
                    # Pointer-like _SimpleCData subclasses can also be converted from
                    # an int or None.
                    allowed_types.append(api.named_generic_type("builtins.int", []))
                    allowed_types.append(NoneType())

    return make_simplified_union(allowed_types)

