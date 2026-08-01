
def read_function_like(data: ReadBuffer, tag: Tag) -> FunctionLike:
    if tag == CALLABLE_TYPE:
        return CallableType.read(data)
    if tag == OVERLOADED:
        return Overloaded.read(data)
    assert False, f"Invalid type tag for FunctionLike {tag}"

