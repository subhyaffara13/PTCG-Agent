
def _sycl_lib_options() -> list[str]:
    """
    Util function for CUTLASS backend to find the correct XPU libraries.
    """
    # _set_gpu_runtime_env()  # cpp_extension consults the env
    from torch.utils import cpp_extension

    lpaths = cpp_extension.library_paths(device_type="xpu")
    extra_ldflags: list[str] = []
    if is_linux():
        for path in lpaths:
            if "torch/lib" in path:
                # don't want to depend on pytorch
                continue
            # -rpath ensures the DLL can find its dependencies when loaded, even
            # if the library path is non-standard.
            extra_ldflags.extend([f"-L{path}", "-Xlinker", f"-rpath={path}"])

        extra_ldflags.append("-lsycl")
    else:
        raise NotImplementedError(
            "Unsupported env, failed to find xpu libs! Currently only Linux is supported."
        )
    return extra_ldflags

