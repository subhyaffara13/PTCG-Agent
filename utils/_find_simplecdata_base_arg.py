
def _find_simplecdata_base_arg(
    tp: Instance, api: mypy.plugin.CheckerPluginInterface
) -> ProperType | None:
    """Try to find a parametrized _SimpleCData in tp's bases and return its single type argument.

    None is returned if _SimpleCData appears nowhere in tp's (direct or indirect) bases.
    """
    if tp.type.has_base("_ctypes._SimpleCData"):
        simplecdata_base = map_instance_to_supertype(
            tp,
            api.named_generic_type("_ctypes._SimpleCData", [AnyType(TypeOfAny.special_form)]).type,
        )
        assert len(simplecdata_base.args) == 1, "_SimpleCData takes exactly one type argument"
        return get_proper_type(simplecdata_base.args[0])
    return None

