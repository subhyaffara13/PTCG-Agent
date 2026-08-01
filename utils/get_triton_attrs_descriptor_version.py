
def get_triton_attrs_descriptor_version() -> TritonAttrsDescriptorVersion:
    if importlib.util.find_spec("triton") is None:
        return TritonAttrsDescriptorVersion.V0_NO_TRITON

    import triton.backends.compiler
    import triton.compiler.compiler

    if hasattr(triton.backends.compiler, "AttrsDescriptor"):
        # Triton 3.2.0
        # AttrsDescriptor was moved from triton.compiler.compiler to triton.backends.compiler.
        # AttrsDescriptor and its serialization format were also changed.

        # TODO: implement V3_BACKENDS_TUPLE
        # On Dec 9, 2024, tuple support (triton #5220) was implemented and breaks handling.
        # We don't have a way to detect this (and haven't implemented this version)
        return TritonAttrsDescriptorVersion.V2_BACKENDS
    elif hasattr(triton.compiler.compiler, "AttrsDescriptor"):
        # Triton 3.0.0
        return TritonAttrsDescriptorVersion.V1_COMPILER
    else:
        # After Jan 1, 2025
        # AttrsDescriptor was removed and replaced with a raw dict.
        return TritonAttrsDescriptorVersion.V4_DICT

