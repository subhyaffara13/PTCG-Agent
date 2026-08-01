
def analyze_decorator_or_funcbase_access(
    defn: Decorator | FuncBase, itype: Instance, name: str, mx: MemberContext
) -> Type:
    """Analyzes the type behind method access.

    The function itself can possibly be decorated.
    See: https://github.com/python/mypy/issues/10409
    """
    if isinstance(defn, Decorator):
        return analyze_var(name, defn.var, itype, mx)
    typ = mx.chk.function_type(defn)
    if isinstance(defn, (FuncDef, OverloadedFuncDef)) and defn.is_trivial_self:
        return bind_self_fast(typ, mx.self_type)
    typ = check_self_arg(typ, mx.self_type, defn.is_class, mx.context, name, mx.msg)
    return bind_self(typ, original_type=mx.self_type, is_classmethod=defn.is_class)

