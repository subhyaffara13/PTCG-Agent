
def _preload_cuda_deps(err: OSError | None = None) -> None:
    cuda_libs: list[tuple[str, str]] = [
        # NOTE: Order matters! We must preload libcublasLt BEFORE libcublas to prevent
        # libcublas from loading a mismatched system-wide libcublasLt via its RUNPATH.
        # Without this, if a different CUDA Toolkit version exists in the system PATH,
        # libcublas may load the wrong libcublasLt, causing symbol errors or runtime failures.
        ("cublas", "libcublasLt.so.*[0-9]"),
        ("cublas", "libcublas.so.*[0-9]"),
        ("cudnn", "libcudnn.so.*[0-9]"),
        ("cuda_nvrtc", "libnvrtc.so.*[0-9]"),
        ("cuda_nvrtc", "libnvrtc-builtins.so.*[0-9]"),
        ("cuda_runtime", "libcudart.so.*[0-9]"),
        ("cuda_cupti", "libcupti.so.*[0-9]"),
        ("cufft", "libcufft.so.*[0-9]"),
        ("curand", "libcurand.so.*[0-9]"),
        ("nvjitlink", "libnvJitLink.so.*[0-9]"),
        ("cusparse", "libcusparse.so.*[0-9]"),
        ("cusparselt", "libcusparseLt.so.*[0-9]"),
        ("cusolver", "libcusolver.so.*[0-9]"),
        ("nccl", "libnccl.so.*[0-9]"),
        ("nvshmem", "libnvshmem_host.so.*[0-9]"),
        ("cufile", "libcufile.so.*[0-9]"),
    ]
    # If error is passed, re-raise it if it's not about one of the abovementioned
    # libraries
    if err is not None and not [
        lib for _, lib in cuda_libs if lib.split(".", 1)[0] in err.args[0]
    ]:
        raise err

    # Otherwise, try to preload dependencies from site-packages
    for lib_folder, lib_name in cuda_libs:
        _preload_cuda_lib(lib_folder, lib_name)

    # libnvToolsExt is Optional Dependency
    _preload_cuda_lib("nvtx", "libnvToolsExt.so.*[0-9]", required=False)

