
def generate_setattr_wrapper(builder: IRBuilder, cdef: ClassDef, setattr: FuncDef) -> None:
    """
    Generate a wrapper function for __setattr__ that can be put into the tp_setattro slot.
    The wrapper takes two arguments besides self - attribute name and the new value.
    Returns 0 on success and -1 on failure. Restrictions are similar to the __getattr__
    wrapper above.

    The wrapper calls the user-defined __setattr__ when the value to set is not NULL.
    When it's NULL, this means that the call to tp_setattro comes from a del statement,
    so it calls __delattr__ instead. If __delattr__ is not overridden in the native class,
    this will call the base implementation in object which doesn't work without __dict__.
    """
    name = setattr.name + "__wrapper"
    ir = builder.mapper.type_to_ir[cdef.info]
    line = setattr.line

    error_base = f'"__setattr__" not supported in class "{cdef.name}" because '
    if ir.allow_interpreted_subclasses:
        builder.error(error_base + "it allows interpreted subclasses", line)
    if ir.inherits_python:
        builder.error(error_base + "it inherits from a non-native class", line)

    with builder.enter_method(ir, name, c_int_rprimitive, internal=True):
        attr_arg = builder.add_argument("attr", object_rprimitive)
        value_arg = builder.add_argument("value", object_rprimitive)

        call_delattr, call_setattr = BasicBlock(), BasicBlock()
        null = Integer(0, object_rprimitive, line)
        is_delattr = builder.add(ComparisonOp(value_arg, null, ComparisonOp.EQ, line))
        builder.add_bool_branch(is_delattr, call_delattr, call_setattr)

        builder.activate_block(call_delattr)
        delattr_symbol = cdef.info.get("__delattr__")
        delattr = delattr_symbol.node if delattr_symbol else None
        delattr_override = delattr is not None and not delattr.fullname.startswith("builtins.")
        if delattr_override:
            builder.gen_method_call(builder.self(), "__delattr__", [attr_arg], None, line)
        else:
            # Call internal function that cpython normally calls when deleting an attribute.
            # Cannot call object.__delattr__ here because it calls PyObject_SetAttr internally
            # which in turn calls our wrapper and recurses infinitely.
            # Note that since native classes don't have __dict__, this will raise AttributeError
            # for dynamic attributes.
            builder.call_c(generic_setattr, [builder.self(), attr_arg, null], line)
        builder.add(Return(Integer(0, c_int_rprimitive), line))

        builder.activate_block(call_setattr)
        builder.gen_method_call(builder.self(), setattr.name, [attr_arg, value_arg], None, line)
        builder.add(Return(Integer(0, c_int_rprimitive), line))

