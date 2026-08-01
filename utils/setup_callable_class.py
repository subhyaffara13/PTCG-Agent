
def setup_callable_class(builder: IRBuilder) -> None:
    """Generate an (incomplete) callable class representing a function.

    This can be a nested function or a function within a non-extension
    class.  Also set up the 'self' variable for that class.

    This takes the most recently visited function and returns a
    ClassIR to represent that function. Each callable class contains
    an environment attribute which points to another ClassIR
    representing the environment class where some of its variables can
    be accessed.

    Note that some methods, such as '__call__', are not yet
    created here. Use additional functions, such as
    add_call_to_callable_class(), to add them.

    Return a newly constructed ClassIR representing the callable
    class for the nested function.
    """
    # Check to see that the name has not already been taken. If so,
    # rename the class. We allow multiple uses of the same function
    # name because this is valid in if-else blocks. Example:
    #
    #     if True:
    #         def foo():          ---->    foo_obj()
    #             return True
    #     else:
    #         def foo():          ---->    foo_obj_0()
    #             return False
    name = base_name = f"{builder.fn_info.namespaced_name()}_obj"
    count = 0
    while name in builder.callable_class_names:
        name = base_name + "_" + str(count)
        count += 1
    builder.callable_class_names.add(name)

    # Define the actual callable class ClassIR, and set its
    # environment to point at the previously defined environment
    # class.
    callable_class_ir = ClassIR(name, builder.module_name, is_generated=True, is_final_class=True)
    callable_class_ir.reuse_freed_instance = True

    # The functools @wraps decorator attempts to call setattr on
    # nested functions, so we create a dict for these nested
    # functions.
    # https://github.com/python/cpython/blob/3.7/Lib/functools.py#L58
    if builder.fn_info.is_nested:
        callable_class_ir.has_dict = True

    # If the enclosing class doesn't contain nested (which will happen if
    # this is a toplevel lambda), don't set up an environment.
    if builder.fn_infos[-2].contains_nested:
        callable_class_ir.attributes[ENV_ATTR_NAME] = RInstance(builder.fn_infos[-2].env_class)
    callable_class_ir.mro = [callable_class_ir]
    builder.fn_info.callable_class = ImplicitClass(callable_class_ir)
    builder.classes.append(callable_class_ir)

    # Add a 'self' variable to the environment of the callable class,
    # and store that variable in a register to be accessed later.
    self_target = builder.add_self_to_env(callable_class_ir)
    builder.fn_info.callable_class.self_reg = builder.read(self_target, builder.fn_info.fitem.line)

    if not builder.fn_info.in_non_ext and builder.fn_info.is_coroutine:
        add_coroutine_properties(builder, callable_class_ir, builder.fn_info.name)

