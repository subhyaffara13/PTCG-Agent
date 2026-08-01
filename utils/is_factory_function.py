
def is_factory_function(f: NativeFunction) -> bool:
    if Variant.function not in f.variants:
        return False

    name = cpp.name(f.func)
    has_tensor_options = python.has_tensor_options(f)
    return has_tensor_options or name.endswith("_like")

