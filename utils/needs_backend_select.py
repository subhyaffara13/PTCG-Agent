
def needs_backend_select(f: NativeFunction, selector: SelectiveBuilder) -> bool:
    name = str(f.func.name.name)
    if name.endswith("_like") or name.startswith("new_"):
        return False
    if f.func.arguments.tensor_options is None:
        return False
    return selector.is_native_function_selected(f)

