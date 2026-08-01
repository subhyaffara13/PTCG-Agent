
def add_coroutine_properties(
    builder: IRBuilder, callable_class_ir: ClassIR, coroutine_name: str
) -> None:
    """Adds properties to the class to make it look like a regular python function.
    Needed to make introspection functions like inspect.iscoroutinefunction work.
    """
    callable_class_ir.coroutine_name = coroutine_name
    callable_class_ir.attributes[CPYFUNCTION_NAME] = object_rprimitive

    properties = {
        "__name__": cpyfunction_get_name,
        "__code__": cpyfunction_get_code,
        "__annotations__": cpyfunction_get_annotations,
        "__defaults__": cpyfunction_get_defaults,
        "__kwdefaults__": cpyfunction_get_kwdefaults,
    }

    writable_props = {
        "__name__": cpyfunction_set_name,
        "__annotations__": cpyfunction_set_annotations,
    }

    line = builder.fn_info.fitem.line

    def get_func_wrapper() -> Value:
        return builder.add(GetAttr(builder.self(), CPYFUNCTION_NAME, line))

    for name, primitive in properties.items():
        with builder.enter_method(callable_class_ir, name, object_rprimitive, internal=True):
            func = get_func_wrapper()
            val = builder.primitive_op(primitive, [func, Integer(0, c_pointer_rprimitive)], line)
            builder.add(Return(val))

    for name, primitive in writable_props.items():
        with builder.enter_method(
            callable_class_ir, f"{PROPSET_PREFIX}{name}", int_rprimitive, internal=True
        ):
            value = builder.add_argument("value", object_rprimitive)
            func = get_func_wrapper()
            rv = builder.primitive_op(
                primitive, [func, value, Integer(0, c_pointer_rprimitive)], line
            )
            builder.add(Return(rv))

    for name in properties:
        getter = callable_class_ir.get_method(name)
        assert getter
        setter = callable_class_ir.get_method(f"{PROPSET_PREFIX}{name}")
        callable_class_ir.properties[name] = (getter, setter)

