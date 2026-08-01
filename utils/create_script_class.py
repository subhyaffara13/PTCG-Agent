
def create_script_class(obj):
    """
    Create and return a RecursiveScriptClass instance from a Python object.

    Arguments:
        obj: A Python object.
    """
    qualified_class_name = _jit_internal._qualified_name(type(obj))
    rcb = _jit_internal.createResolutionCallbackForClassMethods(type(obj))
    # Script the type of obj if it hasn't already been scripted.
    _compile_and_register_class(type(obj), rcb, qualified_class_name)
    class_ty = _python_cu.get_class(qualified_class_name)
    # Create an empty torch._C.ScriptObject with the scripted type.
    cpp_object = torch._C._create_object_with_type(class_ty)
    # Copy all of the attributes over to the torch._C.ScriptObject.
    for name, value in obj.__dict__.items():
        cpp_object.setattr(name, value)

    # Wrap the torch._C.ScriptObject in a RecursiveScriptClass instance.
    return wrap_cpp_class(cpp_object)

