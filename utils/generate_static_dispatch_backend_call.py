
def generate_static_dispatch_backend_call(
    sig: CppSignature | DispatcherSignature,
    f: NativeFunction,
    backend_index: BackendIndex,
) -> str:
    cpp_sig = gen_static_dispatch_backend_call_signature(sig, f)
    name = cpp_sig.name()
    exprs = translate_args(sig, cpp_sig)
    backend_metadata = backend_index.get_kernel(f)
    kernel_ns = (
        backend_metadata.cpp_namespace
        if backend_metadata and backend_metadata.cpp_namespace
        else DEFAULT_KERNEL_NAMESPACE
    )
    ns = kernel_ns.replace("::native", "")
    return f"return {ns}::{backend_index.dispatch_key.lower()}::{name}({exprs});"

