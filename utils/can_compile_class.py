
def can_compile_class(cls) -> bool:
    # If any of the functions on a type don't have a code object, this type can't
    # be compiled and is probably a builtin / bound from C
    if is_ignored_fn(cls):
        return False

    # Ignore the following list of built-in classes.
    ignored_builtin_classes = (torch.nn.Module, tuple, list, Exception)
    if issubclass(cls, ignored_builtin_classes):
        return False

    names = cls.__dict__
    fns = [
        getattr(cls, name)
        for name in names
        if inspect.isroutine(getattr(cls, name, None))
    ]
    has_code = [hasattr(fn, "__code__") for fn in fns]
    return all(has_code)

