
def gen_static_dispatch_backend_call_signature(
    sig: CppSignature | DispatcherSignature,
    f: NativeFunction,
) -> CppSignature:
    sig = DispatcherSignature.from_schema(f.func)
    cpp_sigs = CppSignatureGroup.from_native_function(
        f, method=False, fallback_binding=False
    )
    if sig.symint and f.func.has_symint():
        cpp_sig = cpp_sigs.symint_signature
    else:
        cpp_sig = cpp_sigs.signature
    if cpp_sig is None:
        raise AssertionError(f"No cpp signature found for {f.func.name}")
    return cpp_sig

