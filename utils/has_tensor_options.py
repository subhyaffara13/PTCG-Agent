
def has_tensor_options(f: NativeFunction) -> bool:
    return f.func.arguments.tensor_options is not None

