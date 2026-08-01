
def static_dispatch_ops_header(
    f: NativeFunction, backend_index: list[BackendIndex]
) -> str | None:
    if backend_index is None or f.manual_kernel_registration:
        return None

    output = []
    for index in backend_index:
        dispatch_key = get_static_dispatch_backend(f, index)
        if dispatch_key is not None:
            output.append(
                f"#include <ATen/ops/{f.root_name}_{dispatch_key.lower()}_dispatch.h>"
            )
    return "\n".join(output)

