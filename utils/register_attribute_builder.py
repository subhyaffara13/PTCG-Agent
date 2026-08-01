
def register_attribute_builder(kind, replace=False, allow_existing=False):
    def decorator_builder(func):
        AttrBuilder.insert(kind, func, replace=replace, allow_existing=allow_existing)
        return func

    return decorator_builder

