
def fix_type_var_tuple_argument(t: Instance) -> None:
    if t.type.has_type_var_tuple_type:
        args = list(t.args)
        assert t.type.type_var_tuple_prefix is not None
        tvt = t.type.defn.type_vars[t.type.type_var_tuple_prefix]
        assert isinstance(tvt, TypeVarTupleType)
        args[t.type.type_var_tuple_prefix] = UnpackType(
            Instance(tvt.tuple_fallback.type, [args[t.type.type_var_tuple_prefix]])
        )
        t.args = tuple(args)

