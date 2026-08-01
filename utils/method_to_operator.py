
def method_to_operator(method: str) -> Callable[..., object]:
    return METHOD_TO_OPERATOR[method]

