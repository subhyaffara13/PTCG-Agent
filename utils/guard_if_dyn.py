
def guard_if_dyn(arg: Any) -> Any:
    from .variables import VariableTracker

    arg = specialize_symnode(arg)

    if isinstance(arg, VariableTracker) and arg.is_python_constant():
        return arg.as_python_constant()

    return arg

