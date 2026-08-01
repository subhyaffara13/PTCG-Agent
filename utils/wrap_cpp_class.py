
def wrap_cpp_class(cpp_class):
    """Wrap this torch._C.Object in a Python RecursiveScriptClass."""
    return torch.jit.RecursiveScriptClass(cpp_class)

