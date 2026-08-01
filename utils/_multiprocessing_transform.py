
def _multiprocessing_transform():
    module = parse(
        """
    from multiprocessing.managers import SyncManager
    def Manager():
        return SyncManager()
    """
    )
    # Multiprocessing uses a getattr lookup inside contexts,
    # in order to get the attributes they need. Since it's extremely
    # dynamic, we use this approach to fake it.
    node = parse(
        """
    from multiprocessing.context import DefaultContext, BaseContext
    default = DefaultContext()
    base = BaseContext()
    """
    )
    try:
        context = next(node["default"].infer())
        base = next(node["base"].infer())
    except (InferenceError, StopIteration):
        return module

    for node in (context, base):
        for key, value in node.locals.items():
            if key.startswith("_"):
                continue

            value = value[0]
            if isinstance(value, FunctionDef):
                # We need to rebound this, since otherwise
                # it will have an extra argument (self).
                value = BoundMethod(value, node)
            module[key] = value
    return module

