
def generate_singledispatch_callable_class_ctor(builder: IRBuilder) -> None:
    """Create an __init__ that sets registry and dispatch_cache to empty dicts"""
    line = builder.fn_info.fitem.line
    class_ir = builder.fn_info.callable_class.ir
    with builder.enter_method(class_ir, "__init__", bool_rprimitive):
        empty_dict = builder.call_c(dict_new_op, [], line)
        builder.add(SetAttr(builder.self(), "registry", empty_dict, line))
        cache_dict = builder.call_c(dict_new_op, [], line)
        dispatch_cache_str = builder.load_str("dispatch_cache")
        # use the py_setattr_op instead of SetAttr so that it also gets added to our __dict__
        builder.primitive_op(py_setattr_op, [builder.self(), dispatch_cache_str, cache_dict], line)
        # the generated C code seems to expect that __init__ returns a char, so just return 1
        builder.add(Return(Integer(1, bool_rprimitive, line), line))

