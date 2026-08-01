
def is_symint_or_tensor(arg: Argument) -> bool:
    return arg.type.is_tensor_like() or arg.type.is_symint_like()

