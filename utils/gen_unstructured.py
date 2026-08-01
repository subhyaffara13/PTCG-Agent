
def gen_unstructured(f: NativeFunction, backend_index: BackendIndex) -> str | None:
    sig = kernel_signature(f, backend_index)
    metadata = backend_index.get_kernel(f)
    if metadata is None:
        return None
    if "legacy::" in metadata.kernel:
        return None
    else:
        prefix = "static" if backend_index.external else "TORCH_API"
        return f"{prefix} {sig.decl(name=metadata.kernel)};"

