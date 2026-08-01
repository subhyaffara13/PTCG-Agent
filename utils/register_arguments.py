
def register_arguments(func: nodes.FunctionDef, args: list | None = None) -> None:
    """add given arguments to local

    args is a list that may contains nested lists
    (i.e. def func(a, (b, c, d)): ...)
    """
    # If no args are passed in, get the args from the function.
    if args is None:
        if func.args.vararg:
            func.set_local(func.args.vararg, func.args)
        if func.args.kwarg:
            func.set_local(func.args.kwarg, func.args)
        args = func.args.args
        # If the function has no args, there is nothing left to do.
        if args is None:
            return
    for arg in args:
        if isinstance(arg, nodes.AssignName):
            func.set_local(arg.name, arg)
        else:
            register_arguments(func, arg.elts)

