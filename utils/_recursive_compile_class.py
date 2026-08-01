
def _recursive_compile_class(obj, loc):
    _qual_name = _qualified_name(obj)
    # We're starting a new compilation, so update the error call stack in
    # case it fails
    error_stack = torch._C.CallStack(_qual_name, loc)  # noqa: F841
    rcb = _jit_internal.createResolutionCallbackForClassMethods(obj)
    return _compile_and_register_class(obj, rcb, _qual_name)

