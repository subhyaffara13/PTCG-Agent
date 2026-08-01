
def gen_c_shim(
    func: NativeFunction,
    version_info: dict[str, list[str]],
    func_group_mapping: dict[OperatorName, NativeFunctionsGroup],
    dispatch_key: DispatchKey | None,
    backend_indices: dict[DispatchKey, BackendIndex],
    header: bool,
    extend_aoti_c_shim: bool,
) -> str | None:
    backend_index = get_backend_index_for_aoti(
        func, func_group_mapping, dispatch_key, backend_indices, extend_aoti_c_shim
    )
    if backend_index is None and dispatch_key is not None:
        return None

    schema = func.func
    device = "aten" if dispatch_key is None else dispatch_key.lower()
    backend_call = gen_static_dispatch_backend_call(
        func,
        backend_index,
    )

    try:
        if header:
            declaration, _ = gen_declaration_and_definition(
                schema, device, backend_call, version_info
            )
            return declaration
        else:
            _, definition = gen_declaration_and_definition(
                schema, device, backend_call, version_info
            )
            return definition

    except NotImplementedError:
        return None

