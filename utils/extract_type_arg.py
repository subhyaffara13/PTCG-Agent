
def extract_type_arg(typ: type, index: int) -> type:
    args = get_args(typ)
    try:
        return cast(type, args[index])
    except IndexError as err:
        raise RuntimeError(f"Expected type {typ} to have a type argument at index {index} but it did not") from err

