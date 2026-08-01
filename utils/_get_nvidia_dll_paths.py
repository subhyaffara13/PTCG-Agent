
def _get_nvidia_dll_paths(is_windows: bool, cuda: bool = True, cudnn: bool = True):
    # Dynamically determine CUDA major version from build info
    cuda_major_version = _extract_cuda_major_version(cuda_version)
    cufft_version = _get_cufft_version(cuda_major_version)

    if is_windows:
        # Path is relative to site-packages directory.
        cuda_dll_paths = [
            ("nvidia", "cublas", "bin", f"cublasLt64_{cuda_major_version}.dll"),
            ("nvidia", "cublas", "bin", f"cublas64_{cuda_major_version}.dll"),
            ("nvidia", "cufft", "bin", f"cufft64_{cufft_version}.dll"),
            ("nvidia", "cuda_runtime", "bin", f"cudart64_{cuda_major_version}.dll"),
        ]
        cudnn_dll_paths = [
            ("nvidia", "cudnn", "bin", "cudnn_engines_runtime_compiled64_9.dll"),
            ("nvidia", "cudnn", "bin", "cudnn_engines_precompiled64_9.dll"),
            ("nvidia", "cudnn", "bin", "cudnn_heuristic64_9.dll"),
            ("nvidia", "cudnn", "bin", "cudnn_ops64_9.dll"),
            ("nvidia", "cudnn", "bin", "cudnn_adv64_9.dll"),
            ("nvidia", "cudnn", "bin", "cudnn_graph64_9.dll"),
            ("nvidia", "cudnn", "bin", "cudnn64_9.dll"),
            ("nvidia", "cudnn", "bin", "cudnn_engines_tensor_ir64_9.dll"),
        ]
    else:  # Linux
        # cublas64 depends on cublasLt64, so cublasLt64 should be loaded first.
        cuda_dll_paths = [
            ("nvidia", "cublas", "lib", f"libcublasLt.so.{cuda_major_version}"),
            ("nvidia", "cublas", "lib", f"libcublas.so.{cuda_major_version}"),
            ("nvidia", "cuda_nvrtc", "lib", f"libnvrtc.so.{cuda_major_version}"),
            ("nvidia", "curand", "lib", "libcurand.so.10"),
            ("nvidia", "cufft", "lib", f"libcufft.so.{cufft_version}"),
            ("nvidia", "cuda_runtime", "lib", f"libcudart.so.{cuda_major_version}"),
        ]

        # Do not load cudnn sub DLLs (they will be dynamically loaded later) to be consistent with PyTorch in Linux.
        cudnn_dll_paths = [
            ("nvidia", "cudnn", "lib", "libcudnn.so.9"),
        ]

    return (cuda_dll_paths if cuda else []) + (cudnn_dll_paths if cudnn else [])

