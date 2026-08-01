
def get_out_kernel_name(g: NativeFunctionsGroup, backend_index: BackendIndex) -> str:
    kernel = backend_index.get_kernel(g.out)
    if g.structured or kernel is None:
        return cpp.name(g.out.func)
    return kernel.kernel

