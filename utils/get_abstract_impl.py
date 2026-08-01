
def get_abstract_impl(qualname):
    if qualname not in torch._custom_op.impl.global_registry:
        return None
    custom_op = torch._custom_op.impl.global_registry[qualname]
    if custom_op is None:
        return None
    if not custom_op._has_impl("abstract"):
        return None
    return custom_op._get_impl("abstract").func

