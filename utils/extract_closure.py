
def extract_closure(guard: Any, value: Any) -> Any:
    if type(value) is types.FunctionType and hasattr(value, "__code__"):
        return value.__code__
    return id(value)

