
def gen_attr_descriptor_import() -> str:
    """
    import AttrsDescriptor if the triton version is new enough to have this
    class defined.
    """
    if not has_triton_package():
        return ""

    import triton.compiler.compiler

    # Note: this works because triton.compiler.compiler imports AttrsDescriptor from triton.backends.compiler
    # When support for the legacy AttrsDescriptor is removed then this import path should be changed.
    if hasattr(triton.compiler.compiler, "AttrsDescriptor"):
        return "from triton.compiler.compiler import AttrsDescriptor"
    else:
        return ""

