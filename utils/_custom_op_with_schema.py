
def _custom_op_with_schema(qualname, schema, needs_fixed_stride_order=True):
    ns, name = qualname.split("::")
    schema_str = f"{name}{schema}"
    function_schema = FunctionSchema.parse(schema_str)
    validate_schema(function_schema)
    tags = [torch._C.Tag.needs_fixed_stride_order] if needs_fixed_stride_order else []
    lib = library.Library(ns, "FRAGMENT")
    lib.define(schema_str, tags=tags)
    ophandle = find_ophandle_or_throw(ns, function_schema.name)
    result = CustomOp(lib, ns, function_schema, name, ophandle, _private_access=True)
    result._register_autograd_kernel_indirection()

    torch._C._dispatch_set_report_error_callback(
        ophandle, functools.partial(report_error_callback, weakref.proxy(result))
    )
    return get_op(qualname)

