
def get_base_name(f: NativeFunction) -> str:
    return f.func.name.name.base  # TODO: should be str(f.func.name.name)?

