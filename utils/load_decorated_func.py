
def load_decorated_func(builder: IRBuilder, fdef: FuncDef, orig_func_reg: Value) -> Value:
    """Apply decorators to a function.

    Given a decorated FuncDef and an instance of the callable class
    representing that FuncDef, apply the corresponding decorator
    functions on that decorated FuncDef and return the decorated
    function.
    """
    if not is_decorated(builder, fdef):
        # If there are no decorators associated with the function, then just return the
        # original function.
        return orig_func_reg

    decorators = builder.fdefs_to_decorators[fdef]
    func_reg = orig_func_reg
    for d in reversed(decorators):
        decorator = d.accept(builder.visitor)
        assert isinstance(decorator, Value), decorator
        func_reg = builder.py_call(decorator, [func_reg], func_reg.line)
    return func_reg

