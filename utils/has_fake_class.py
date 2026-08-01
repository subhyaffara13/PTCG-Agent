
def has_fake_class(full_qualname) -> bool:
    return global_fake_class_registry.has_impl(full_qualname)

