
def gen_static_dispatch_backend_call(
    f: NativeFunction,
    backend_index: BackendIndex | None = None,
) -> str:
    sig = DispatcherSignature.from_schema(f.func)
    cpp_sig = gen_static_dispatch_backend_call_signature(sig, f)

    if backend_index is None:
        # Check if this is a symint function and if the function only has method variants
        if sig.symint and f.func.has_symint():
            has_function_variant = Variant.function in f.variants

            if not has_function_variant:
                # Functions with both function and method variants can use the at::{*}_symint version
                # (e.g., narrow -> at::narrow_symint), BUT
                # Method-only functions with symint parameters should use at::symint:: namespace
                # Remove the _symint suffix since at::symint:: namespace uses the base name
                # (e.g., new_empty -> at::symint::new_empty<c10::SymInt>)
                base_name = cpp_sig.name()
                base_name = base_name.removesuffix("_symint")  # Remove "_symint" suffix
                return f"at::symint::{base_name}<c10::SymInt>"

        return f"at::{cpp_sig.name()}"
    else:
        return f"at::{backend_index.dispatch_key.lower()}::{cpp_sig.name()}"

