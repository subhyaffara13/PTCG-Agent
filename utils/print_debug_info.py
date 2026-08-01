
def print_debug_info():
    """Print information to help debugging."""
    import importlib.util  # noqa: PLC0415
    import os  # noqa: PLC0415
    import platform  # noqa: PLC0415
    from importlib.metadata import distributions  # noqa: PLC0415

    print(f"{package_name} version: {__version__}")
    if cuda_version:
        print(f"CUDA version used in build: {cuda_version}")
    print("platform:", platform.platform())

    print("\nPython package, version and location:")
    ort_packages = []
    for dist in distributions():
        package = dist.metadata["Name"]
        if package == "onnxruntime" or package.startswith(("onnxruntime-", "ort-")):
            # Exclude packages whose root directory name is not onnxruntime.
            location = _get_package_root(package, "onnxruntime")
            if location and (package not in ort_packages):
                ort_packages.append(package)
                print(f"{package}=={dist.version} at {location}")

    if len(ort_packages) > 1:
        print(
            "\033[33mWARNING: multiple onnxruntime packages are installed to the same location. "
            "Please 'pip uninstall` all above packages, then `pip install` only one of them.\033[0m"
        )

    if cuda_version:
        # Print version of installed packages that is related to CUDA or cuDNN DLLs.
        cuda_major = _extract_cuda_major_version(cuda_version)

        packages = [
            "torch",
            f"nvidia-cuda-runtime-cu{cuda_major}",
            f"nvidia-cudnn-cu{cuda_major}",
            f"nvidia-cublas-cu{cuda_major}",
            f"nvidia-cufft-cu{cuda_major}",
            f"nvidia-curand-cu{cuda_major}",
            f"nvidia-cuda-nvrtc-cu{cuda_major}",
            f"nvidia-nvjitlink-cu{cuda_major}",
        ]
        for package in packages:
            directory_name = "nvidia" if package.startswith("nvidia-") else None
            version = _get_package_version(package)
            if version:
                print(f"{package}=={version} at {_get_package_root(package, directory_name)}")
            else:
                print(f"{package} not installed")

    if platform.system() == "Windows":
        print(f"\nEnvironment variable:\nPATH={os.environ.get('PATH', '(unset)')}")
    elif platform.system() == "Linux":
        print(f"\nEnvironment variable:\nLD_LIBRARY_PATH={os.environ.get('LD_LIBRARY_PATH', '(unset)')}")

    if importlib.util.find_spec("psutil"):

        def is_target_dll(path: str):
            target_keywords = ["vcruntime140", "msvcp140"]
            if cuda_version:
                target_keywords = ["cufft", "cublas", "cudart", "nvrtc", "curand", "cudnn", *target_keywords]
            return any(keyword in path for keyword in target_keywords)

        import psutil  # noqa: PLC0415

        p = psutil.Process(os.getpid())

        print("\nList of loaded DLLs:")
        for lib in p.memory_maps():
            if is_target_dll(lib.path.lower()):
                print(lib.path)

        if cuda_version:
            if importlib.util.find_spec("cpuinfo") and importlib.util.find_spec("py3nvml"):
                from .transformers.machine_info import get_device_info  # noqa: PLC0415

                print("\nDevice information:")
                print(get_device_info())
            else:
                print("please `pip install py-cpuinfo py3nvml` to show device information.")
    else:
        print("please `pip install psutil` to show loaded DLLs.")

