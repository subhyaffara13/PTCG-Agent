
def expand_self_type_if_needed(
    t: Type, mx: MemberContext, var: Var, itype: Instance, is_class: bool = False
) -> Type:
    """Expand special Self type in a backwards compatible manner.

    This should ensure that mixing old-style and new-style self-types work
    seamlessly. Also, re-bind new style self-types in subclasses if needed.
    """
    original = get_proper_type(mx.self_type)
    if not (mx.is_self or mx.is_super):
        repl = mx.self_type
        if is_class:
            if isinstance(original, TypeType):
                repl = original.item
            elif isinstance(original, CallableType):
                # Problematic access errors should have been already reported.
                repl = erase_typevars(original.ret_type)
            else:
                repl = itype
        return expand_self_type(var, t, repl)
    elif supported_self_type(
        # Support compatibility with plain old style T -> T and Type[T] -> T only.
        get_proper_type(mx.self_type),
        allow_instances=False,
        allow_callable=False,
    ):
        repl = mx.self_type
        if is_class and isinstance(original, TypeType):
            repl = original.item
        return expand_self_type(var, t, repl)
    elif (
        mx.is_self
        and itype.type != var.info
        # If an attribute with Self-type was defined in a supertype, we need to
        # rebind the Self type variable to Self type variable of current class...
        and itype.type.self_type is not None
        # ...unless `self` has an explicit non-trivial annotation.
        and itype == mx.chk.scope.active_self_type()
    ):
        return expand_self_type(var, t, itype.type.self_type)
    else:
        return t

