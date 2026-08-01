
def requires_nvshmem(  # type: ignore[no-untyped-def]
    jit_func,  # JITFunction created by triton.jit
):
    """
    A decorator to register a Triton kernel function that requires NVSHMEM initialization.

    Example usage:
    ```
        @requires_nvshmem
        @triton.jit
        def foo(...):
            ...
    ```

    If you would like to specify a path to the NVSHMEM device library other
    than standard search locations, you can use the following environment
    variable:
    ```
        export NVSHMEM_LIB_DIR=/path/to/nvshmem/lib
    ```
    """

    import triton
    from triton.runtime.jit import JITFunction

    if not isinstance(jit_func, JITFunction):
        raise TypeError(f"Expected a JITFunction, but got {type(jit_func)}")

    # Find the NVSHMEM device library
    lib_path = NvshmemLibFinder.find_device_library()
    extern_libs = {"libnvshmem_device": lib_path}

    # Register the JITFunction with the kernel registry as "to be initialized"
    NvshmemKernelRegistry.register(jit_func.fn.__name__)

    # Register the NVSHMEM init function as a post-compile hook.
    # [Note] This is a global setting (due to lack of Triton API exposure). To
    # avoid initializing Triton kernels that do not require NVSHMEM, filtering
    # is performed in the hook function itself by checking against
    # NvshmemKernelRegistry.
    triton.knobs.runtime.jit_post_compile_hook = _nvshmem_init_hook

    return GridCallableWithExtern(jit_func, extern_libs)

