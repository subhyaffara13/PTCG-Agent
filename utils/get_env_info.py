import sys

def get_env_info():
    """
    Collects environment information to aid in debugging.

    The returned environment information contains details on torch version, is debug build
    or not, cuda compiled version, gcc version, clang version, cmake version, operating
    system, libc version, python version, python platform, CUDA availability, CUDA
    runtime version, CUDA module loading config, GPU model and configuration, Nvidia
    driver version, cuDNN version, pip version and versions of relevant pip and
    conda packages, HIP runtime version, MIOpen runtime version,
    Caching allocator config, XNNPACK availability and CPU information.

    Returns:
        SystemEnv (namedtuple): A tuple containing various environment details
            and system information.
    """
    run_lambda = run
    pip_version, pip_list_output = get_pip_packages(run_lambda)

    if TORCH_AVAILABLE:
        version_str = torch.__version__
        debug_mode_str = str(torch.version.debug)
        cuda_available_str = str(torch.cuda.is_available())
        cuda_version_str = torch.version.cuda
        xpu_available_str = str(torch.xpu.is_available())
        if torch.xpu.is_available():
            xpu_available_str = (
                f"{xpu_available_str}\n"
                + f"XPU used to build PyTorch: {torch.version.xpu}\n"
                + f"Intel GPU driver version:\n{get_intel_gpu_driver_version(run_lambda)}\n"
                + f"Intel GPU models onboard:\n{get_intel_gpu_onboard(run_lambda)}\n"
                + f"Intel GPU models detected:\n{get_intel_gpu_detected(run_lambda)}"
            )
        if (
            not hasattr(torch.version, "hip") or torch.version.hip is None
        ):  # cuda version
            hip_compiled_version = hip_runtime_version = miopen_runtime_version = "N/A"
        else:  # HIP version

            def get_version_or_na(cfg, prefix):
                _lst = [s.rsplit(None, 1)[-1] for s in cfg if prefix in s]
                return _lst[0] if _lst else "N/A"

            cfg = torch._C._show_config().split("\n")
            hip_runtime_version = get_version_or_na(cfg, "HIP Runtime")
            miopen_runtime_version = get_version_or_na(cfg, "MIOpen")
            cuda_version_str = "N/A"
            hip_compiled_version = torch.version.hip
    else:
        version_str = debug_mode_str = cuda_available_str = cuda_version_str = xpu_available_str = "N/A"  # type: ignore[assignment]
        hip_compiled_version = hip_runtime_version = miopen_runtime_version = "N/A"

    sys_version = sys.version.replace("\n", " ")

    conda_packages = get_conda_packages(run_lambda)

    return SystemEnv(
        torch_version=version_str,
        is_debug_build=debug_mode_str,
        python_version="{} ({}-bit runtime)".format(
            sys_version, sys.maxsize.bit_length() + 1
        ),
        python_platform=get_python_platform(),
        is_cuda_available=cuda_available_str,
        cuda_compiled_version=cuda_version_str,
        cuda_runtime_version=get_running_cuda_version(run_lambda),
        cuda_module_loading=get_cuda_module_loading_config(),
        nvidia_gpu_models=get_gpu_info(run_lambda),
        nvidia_driver_version=get_nvidia_driver_version(run_lambda),
        cudnn_version=get_cudnn_version(run_lambda),
        is_xpu_available=xpu_available_str,
        hip_compiled_version=hip_compiled_version,
        hip_runtime_version=hip_runtime_version,
        miopen_runtime_version=miopen_runtime_version,
        pip_version=pip_version,
        pip_packages=pip_list_output,
        conda_packages=conda_packages,
        os=get_os(run_lambda),
        libc_version=get_libc_version(),
        gcc_version=get_gcc_version(run_lambda),
        clang_version=get_clang_version(run_lambda),
        cmake_version=get_cmake_version(run_lambda),
        caching_allocator_config=get_cachingallocator_config(),
        is_xnnpack_available=is_xnnpack_available(),
        cpu_info=get_cpu_info(run_lambda),
    )

