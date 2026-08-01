
def kernel_name(g: NativeFunctionsGroup, dispatch_key: DispatchKey) -> str:
    return schema_kernel_name(g.out.func, dispatch_key)

