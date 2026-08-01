
def freshen_function_type_vars(callee: F) -> F:
    """Substitute fresh type variables for generic function type variables."""
    if isinstance(callee, CallableType):
        if not callee.is_generic():
            return callee
        tvs = []
        tvmap: dict[TypeVarId, Type] = {}
        for v in callee.variables:
            tv = v.new_unification_variable(v)
            tvs.append(tv)
            tvmap[v.id] = tv
            if tv.has_default():
                # Point to fresh ids in case defaults depend on previous variables.
                tv.default = expand_type(tv.default, tvmap)
        fresh = expand_type(callee, tvmap).copy_modified(variables=tvs)
        return cast(F, fresh)
    else:
        assert isinstance(callee, Overloaded)
        fresh_overload = Overloaded([freshen_function_type_vars(item) for item in callee.items])
        return cast(F, fresh_overload)

