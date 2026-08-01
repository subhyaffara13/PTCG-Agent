
def _resolve_warning_category(category: str) -> type[Warning]:
    """
    Copied from warnings._getcategory, but changed so it lets exceptions (specially ImportErrors)
    propagate so we can get access to their tracebacks (#9218).
    """
    __tracebackhide__ = True
    if not category:
        return Warning

    if "." not in category:
        import builtins as m

        klass = category
    else:
        module, _, klass = category.rpartition(".")
        m = importlib.import_module(module)
    cat = getattr(m, klass)
    if not issubclass(cat, Warning):
        raise UsageError(f"{cat} is not a Warning subclass")
    return cast(type[Warning], cat)

