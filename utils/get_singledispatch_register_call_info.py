
def get_singledispatch_register_call_info(
    decorator: Expression, func: FuncDef
) -> RegisteredImpl | None:
    # @fun.register(complex)
    # def g(arg): ...
    if (
        isinstance(decorator, CallExpr)
        and len(decorator.args) == 1
        and isinstance(decorator.args[0], RefExpr)
    ):
        callee = decorator.callee
        dispatch_type = decorator.args[0].node
        if not isinstance(dispatch_type, TypeInfo):
            return None

        if isinstance(callee, MemberExpr):
            return registered_impl_from_possible_register_call(callee, dispatch_type)
    # @fun.register
    # def g(arg: int): ...
    elif isinstance(decorator, MemberExpr):
        # we don't know if this is a register call yet, so we can't be sure that the function
        # actually has arguments
        if not func.arguments:
            return None
        arg_type = get_proper_type(func.arguments[0].variable.type)
        if not isinstance(arg_type, Instance):
            return None
        info = arg_type.type
        return registered_impl_from_possible_register_call(decorator, info)
    return None

