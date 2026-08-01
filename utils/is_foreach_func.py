
def is_foreach_func(f: NativeFunction) -> bool:
    return f.func.name.name.base.startswith("_foreach_")

