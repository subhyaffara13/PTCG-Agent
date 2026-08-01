
def setup_non_ext_dict(
    builder: IRBuilder, cdef: ClassDef, metaclass: Value, bases: Value
) -> Value:
    """Initialize the class dictionary for a non-extension class.

    This class dictionary is passed to the metaclass constructor.
    """
    # Check if the metaclass defines a __prepare__ method, and if so, call it.
    has_prepare = builder.primitive_op(
        py_hasattr_op, [metaclass, builder.load_str("__prepare__")], cdef.line
    )

    non_ext_dict = Register(dict_rprimitive)

    true_block, false_block, exit_block = BasicBlock(), BasicBlock(), BasicBlock()
    builder.add_bool_branch(has_prepare, true_block, false_block)

    builder.activate_block(true_block)
    cls_name = builder.load_str(cdef.name)
    prepare_meth = builder.py_get_attr(metaclass, "__prepare__", cdef.line)
    prepare_dict = builder.py_call(prepare_meth, [cls_name, bases], cdef.line)
    builder.assign(non_ext_dict, prepare_dict, cdef.line)
    builder.goto(exit_block)

    builder.activate_block(false_block)
    builder.assign(non_ext_dict, builder.call_c(dict_new_op, [], cdef.line), cdef.line)
    builder.goto(exit_block)
    builder.activate_block(exit_block)

    return non_ext_dict

