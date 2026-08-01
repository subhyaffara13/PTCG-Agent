
def setup_env_for_generator_class(builder: IRBuilder) -> None:
    """Populates the environment for a generator class."""
    fitem = builder.fn_info.fitem
    cls = builder.fn_info.generator_class
    self_target = builder.add_self_to_env(cls.ir)

    # Add the type, value, and traceback variables to the environment.
    exc_type = builder.add_local(Var("type"), object_rprimitive, is_arg=True)
    exc_val = builder.add_local(Var("value"), object_rprimitive, is_arg=True)
    exc_tb = builder.add_local(Var("traceback"), object_rprimitive, is_arg=True)
    # TODO: Use the right type here instead of object?
    exc_arg = builder.add_local(Var("arg"), object_rprimitive, is_arg=True)

    # Parameter that can used to pass a pointer which can used instead of
    # raising StopIteration(value). If the value is NULL, this won't be used.
    stop_iter_value_arg = builder.add_local(
        Var("stop_iter_ptr"), object_pointer_rprimitive, is_arg=True
    )

    cls.exc_regs = (exc_type, exc_val, exc_tb)
    cls.send_arg_reg = exc_arg
    cls.stop_iter_value_reg = stop_iter_value_arg

    cls.self_reg = builder.read(self_target, fitem.line)
    if builder.fn_info.can_merge_generator_and_env_classes():
        cls.curr_env_reg = cls.self_reg
    else:
        cls.curr_env_reg = load_outer_env(builder, cls.self_reg, builder.symtables[-1])

    # Define a variable representing the label to go to the next time
    # the '__next__' function of the generator is called, and add it
    # as an attribute to the environment class.
    cls.next_label_target = builder.add_var_to_env_class(
        Var(NEXT_LABEL_ATTR_NAME), int32_rprimitive, cls, reassign=False, always_defined=True
    )

    # Add arguments from the original generator function to the
    # environment of the generator class.
    add_args_to_env(
        builder, local=False, base=cls, reassign=False, prefix=GENERATOR_ATTRIBUTE_PREFIX
    )

    # Set the next label register for the generator class.
    cls.next_label_reg = builder.read(cls.next_label_target, fitem.line)

