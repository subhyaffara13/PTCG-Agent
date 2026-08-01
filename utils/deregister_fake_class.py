
def deregister_fake_class(qualname):
    return global_fake_class_registry.deregister(_full_qual_class_name(qualname))

