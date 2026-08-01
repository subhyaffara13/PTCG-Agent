
def type_wrapper_name(f: NativeFunction, key: str = "Default") -> str:
    if f.func.name.overload_name:
        name = f"{cpp.name(f.func)}_{f.func.name.overload_name}"
    else:
        name = cpp.name(f.func)

    # The key argument is only used in gen_variable_type where we need fns per autograd dispatch key.
    # In gen_trace_type and gen_inplace_view_type where only one fn per native_fn must be generated,
    # the key argument should not be passed.
    # We do not append key if it is Default so that generated functions from
    # before per-dispatch-key derivatives were added retain the same names.
    if key != "Default":
        name = name + f"_{key}"
    return name

