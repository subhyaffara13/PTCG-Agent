
def preload_dlls(cuda: bool = True, cudnn: bool = True, msvc: bool = True, directory=None):
    """Preload CUDA 12.x+ and cuDNN 9.x DLLs in Windows or Linux, and MSVC runtime DLLs in Windows.

       When the installed PyTorch is compatible (using same major version of CUDA and cuDNN),
       there is no need to call this function if `import torch` is done before `import onnxruntime`.

    Args:
        cuda (bool, optional): enable loading CUDA DLLs. Defaults to True.
        cudnn (bool, optional): enable loading cuDNN DLLs. Defaults to True.
        msvc (bool, optional): enable loading MSVC DLLs in Windows. Defaults to True.
        directory(str, optional): a directory contains CUDA or cuDNN DLLs. It can be an absolute path,
           or a path relative to the directory of this file.
           If directory is None (default value), the search order: the lib directory of compatible PyTorch in Windows,
            nvidia site packages, default DLL loading paths.
           If directory is empty string (""), the search order: nvidia site packages, default DLL loading paths.
           If directory is a path, the search order: the directory, default DLL loading paths.
    """
    import ctypes  # noqa: PLC0415
    import os  # noqa: PLC0415
    import platform  # noqa: PLC0415
    import sys  # noqa: PLC0415

    if platform.system() not in ["Windows", "Linux"]:
        return

    is_windows = platform.system() == "Windows"
    if is_windows and msvc:
        try:
            ctypes.CDLL("vcruntime140.dll")
            ctypes.CDLL("msvcp140.dll")
            if platform.machine() != "ARM64":
                ctypes.CDLL("vcruntime140_1.dll")
        except OSError:
            print("Microsoft Visual C++ Redistributable is not installed, this may lead to the DLL load failure.")
            print("It can be downloaded at https://aka.ms/vs/17/release/vc_redist.x64.exe.")

    # Check if CUDA version is supported (12.x or 13.x+)
    ort_cuda_major = None
    if cuda_version:
        try:
            ort_cuda_major = int(cuda_version.split(".")[0])
            if ort_cuda_major < 12 and (cuda or cudnn):
                print(
                    f"\033[33mWARNING: {package_name} is built with CUDA {cuda_version}, which is not supported for preloading. "
                    f"CUDA 12.x or newer is required. Call preload_dlls with cuda=False and cudnn=False.\033[0m"
                )
                return
        except ValueError:
            print(
                f"\033[33mWARNING: Unable to parse CUDA version '{cuda_version}'. "
                "Skipping DLL preloading. Call preload_dlls with cuda=False and cudnn=False.\033[0m"
            )
            return
    elif cuda or cudnn:
        # No CUDA version info available but CUDA/cuDNN preloading requested
        return

    is_cuda_cudnn_imported_by_torch = False

    if is_windows:
        torch_version = _get_package_version("torch")
        # Check if torch CUDA version matches onnxruntime CUDA version
        torch_cuda_major = None
        if torch_version and "+cu" in torch_version:
            with contextlib.suppress(ValueError):
                # Extract CUDA version from torch (e.g., "2.0.0+cu121" -> 12)
                cu_part = torch_version.split("+cu")[1]
                torch_cuda_major = int(cu_part[:2])  # First 2 digits are major version

        is_torch_cuda_compatible = (
            torch_cuda_major == ort_cuda_major if (torch_cuda_major and ort_cuda_major) else False
        )

        if "torch" in sys.modules:
            is_cuda_cudnn_imported_by_torch = is_torch_cuda_compatible
            if torch_cuda_major and ort_cuda_major and torch_cuda_major != ort_cuda_major:
                print(
                    f"\033[33mWARNING: The installed PyTorch {torch_version} uses CUDA {torch_cuda_major}.x, "
                    f"but {package_name} is built with CUDA {ort_cuda_major}.x. "
                    f"Please install PyTorch for CUDA {ort_cuda_major}.x to be compatible.\033[0m"
                )

        if is_torch_cuda_compatible and directory is None:
            torch_root = _get_package_root("torch", "torch")
            if torch_root:
                directory = os.path.join(torch_root, "lib")

    base_directory = directory or ".."
    if not os.path.isabs(base_directory):
        base_directory = os.path.join(os.path.dirname(__file__), base_directory)
    base_directory = os.path.normpath(base_directory)
    if not os.path.isdir(base_directory):
        raise RuntimeError(f"Invalid parameter of directory={directory}. The directory does not exist!")

    if is_cuda_cudnn_imported_by_torch:
        # In Windows, PyTorch has loaded CUDA and cuDNN DLLs during `import torch`, no need to load them again.
        print("Skip loading CUDA and cuDNN DLLs since torch is imported.")
        return

    # Try load DLLs from nvidia site packages.
    dll_paths = _get_nvidia_dll_paths(is_windows, cuda, cudnn)
    loaded_dlls = []
    for relative_path in dll_paths:
        dll_path = (
            os.path.join(base_directory, relative_path[-1])
            if directory
            else os.path.join(base_directory, *relative_path)
        )
        if os.path.isfile(dll_path):
            try:
                _ = ctypes.CDLL(dll_path)
                loaded_dlls.append(relative_path[-1])
            except Exception as e:
                print(f"Failed to load {dll_path}: {e}")

    # cuDNN DLLs that only exist in newer cuDNN releases (e.g. >= 9.23) and are
    # optional for inference. Missing them on older cuDNN must not be treated as a failure.
    _optional_dll_filenames = {"cudnn_engines_tensor_ir64_9.dll"}

    # Try load DLLs with default path settings.
    has_failure = False
    for relative_path in dll_paths:
        dll_filename = relative_path[-1]
        if dll_filename not in loaded_dlls:
            try:
                _ = ctypes.CDLL(dll_filename)
            except Exception as e:
                if dll_filename not in _optional_dll_filenames:
                    has_failure = True
                    print(f"Failed to load {dll_filename}: {e}")

    if has_failure:
        print("Please follow https://onnxruntime.ai/docs/install/#cuda-and-cudnn to install CUDA and CuDNN.")

