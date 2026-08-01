
def cpp_dispatch_target(f: NativeFunction) -> str:
    symint = f.func.has_symint()
    name = cpp.name(f.func, symint_overload=symint)
    if Variant.method in f.variants:
        return f"self.{name}"
    if Variant.function in f.variants:
        if has_tensor_options(f) or f.func.name.name.base.endswith("_like"):
            namespace = "torch"
        else:
            namespace = "at"
        return f"{namespace}::{name}"
    raise RuntimeError(f"could not dispatch, neither function nor method: {f.func}")

