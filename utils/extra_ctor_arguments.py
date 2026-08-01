
def extra_ctor_arguments(func: FunctionSchema) -> list[Binding]:
    return attributes(func, owning=False)

