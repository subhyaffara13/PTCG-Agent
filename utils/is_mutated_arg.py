
def is_mutated_arg(argument: Argument) -> bool:
    return argument.annotation is not None and argument.annotation.is_write

