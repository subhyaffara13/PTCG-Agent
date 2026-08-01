
def get_property_stubs(nn_module):
    """Create property stubs for the properties of the module by creating method stubs for the getter and setter."""
    module_ty = type(nn_module)
    properties_asts = get_class_properties(module_ty, self_name="RecursiveScriptModule")
    rcbs = {}

    for name in dir(module_ty):
        item = getattr(module_ty, name, None)
        if isinstance(item, property):
            if not item.fget:
                raise RuntimeError(
                    f"Property {name} of {nn_module.__name__} must have a getter"
                )

            rcbs[name] = _jit_internal.createResolutionCallbackFromClosure(item.fget)

    stubs = [PropertyStub(rcbs[ast.name().name], ast) for ast in properties_asts]
    return stubs

