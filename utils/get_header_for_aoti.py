
def get_header_for_aoti(
    func: NativeFunction,
    func_group_mapping: dict[OperatorName, NativeFunctionsGroup],
    dispatch_key: DispatchKey | None,
    backend_indices: dict[DispatchKey, BackendIndex],
    extend_aoti_c_shim: bool,
) -> str | None:
    backend_index = get_backend_index_for_aoti(
        func, func_group_mapping, dispatch_key, backend_indices, extend_aoti_c_shim
    )
    if backend_index is None:
        if dispatch_key is None:
            return f"#include <ATen/ops/{func.root_name}.h>"
        return None

    return f"#include <ATen/ops/{func.root_name}_{backend_index.dispatch_key.lower()}_dispatch.h>"

