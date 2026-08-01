
def generate_getattr_wrapper(builder: IRBuilder, cdef: ClassDef, getattr: FuncDef) -> None:
    """
    Generate a wrapper function for __getattr__ that can be put into the tp_getattro slot.
    The wrapper takes one argument besides self which is the attribute name.
    It first checks if the name matches any of the attributes of this class.
    If it does, it returns that attribute. If none match, it calls __getattr__.

    __getattr__ is not supported in classes that allow interpreted subclasses because the
    tp_getattro slot is inherited by subclasses and if the subclass overrides __getattr__,
    the override would be ignored in our wrapper. TODO: To support this, the wrapper would
    have to check type of self and if it's not the compiled class, resolve "__getattr__" against
    the type at runtime and call the returned method, like _Py_slot_tp_getattr_hook in cpython.

    __getattr__ is not supported in classes which inherit from non-native classes because those
    have __dict__ which currently has some strange interactions when class attributes and
    variables are assigned through __dict__ vs. through regular attribute access. Allowing
    __getattr__ on top of that could be problematic.
    """
    name = getattr.name + "__wrapper"
    ir = builder.mapper.type_to_ir[cdef.info]
    line = getattr.line

    error_base = f'"__getattr__" not supported in class "{cdef.name}" because '
    if ir.allow_interpreted_subclasses:
        builder.error(error_base + "it allows interpreted subclasses", line)
    if ir.inherits_python:
        builder.error(error_base + "it inherits from a non-native class", line)

    with builder.enter_method(ir, name, object_rprimitive, internal=True):
        attr_arg = builder.add_argument("attr", object_rprimitive)
        generic_getattr_result = builder.call_c(generic_getattr, [builder.self(), attr_arg], line)

        return_generic, call_getattr = BasicBlock(), BasicBlock()
        null = Integer(0, object_rprimitive, line)
        got_generic = builder.add(
            ComparisonOp(generic_getattr_result, null, ComparisonOp.NEQ, line)
        )
        builder.add_bool_branch(got_generic, return_generic, call_getattr)

        builder.activate_block(return_generic)
        builder.add(Return(generic_getattr_result, line))

        builder.activate_block(call_getattr)
        # No attribute matched so call user-provided __getattr__.
        getattr_result = builder.gen_method_call(
            builder.self(), getattr.name, [attr_arg], object_rprimitive, line
        )
        builder.add(Return(getattr_result, line))

