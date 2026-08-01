
def instantiate_generator_class(builder: IRBuilder) -> Value:
    fitem = builder.fn_info.fitem
    generator_reg = builder.add(Call(builder.fn_info.generator_class.ir.ctor, [], fitem.line))

    if builder.fn_info.can_merge_generator_and_env_classes():
        # Set the generator instance to the initial state (zero).
        zero = Integer(0)
        builder.add(SetAttr(generator_reg, NEXT_LABEL_ATTR_NAME, zero, fitem.line))
    else:
        # Get the current environment register. If the current function is nested, then the
        # generator class gets instantiated from the callable class' '__call__' method, and hence
        # we use the callable class' environment register. Otherwise, we use the original
        # function's environment register.
        if builder.fn_info.is_nested:
            curr_env_reg = builder.fn_info.callable_class.curr_env_reg
        else:
            curr_env_reg = builder.fn_info.curr_env_reg

        # Set the generator class' environment attribute to point at the environment class
        # defined in the current scope.
        builder.add(SetAttr(generator_reg, ENV_ATTR_NAME, curr_env_reg, fitem.line))

        # Set the generator instance's environment to the initial state (zero).
        zero = Integer(0)
        builder.add(SetAttr(curr_env_reg, NEXT_LABEL_ATTR_NAME, zero, fitem.line))
    return generator_reg

