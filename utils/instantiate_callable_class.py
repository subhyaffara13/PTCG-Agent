
def instantiate_callable_class(builder: IRBuilder, fn_info: FuncInfo) -> Value:
    """Create an instance of a callable class for a function.

    Calls to the function will actually call this instance.

    Note that fn_info refers to the function being assigned, whereas
    builder.fn_info refers to the function encapsulating the function
    being turned into a callable class.
    """
    fitem = fn_info.fitem
    func_reg = builder.add(Call(fn_info.callable_class.ir.ctor, [], fitem.line))

    # Set the environment attribute of the callable class to point at
    # the environment class defined in the callable class' immediate
    # outer scope. Note that there are three possible environment
    # class registers we may use. This depends on what the encapsulating
    # (parent) function is:
    #
    # - A nested function: the callable class is instantiated
    #   from the current callable class' '__call__' function, and hence
    #   the callable class' environment register is used.
    # - A generator function: the callable class is instantiated
    #   from the '__next__' method of the generator class, and hence the
    #   environment of the generator class is used.
    # - Regular function or comprehension scope: we use the environment
    #   of the original function. Comprehension scopes are inlined (no
    #   callable class), so they fall into this case despite is_nested.
    curr_env_reg = None
    if builder.fn_info.is_generator:
        curr_env_reg = builder.fn_info.generator_class.curr_env_reg
    elif builder.fn_info.is_nested and not builder.fn_info.is_comprehension_scope:
        curr_env_reg = builder.fn_info.callable_class.curr_env_reg
    elif builder.fn_info.contains_nested:
        curr_env_reg = builder.fn_info.curr_env_reg
    if curr_env_reg:
        builder.add(SetAttr(func_reg, ENV_ATTR_NAME, curr_env_reg, fitem.line))
    # Initialize function wrapper for callable classes. As opposed to regular functions,
    # each instance of a callable class needs its own wrapper because they might be instantiated
    # inside other functions.
    if not fn_info.in_non_ext and fn_info.is_coroutine:
        builder.add_coroutine_setup_call(fn_info.callable_class.ir.name, func_reg)
    return func_reg

