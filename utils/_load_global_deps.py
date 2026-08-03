import os

def _load_global_deps() -> None:
    if platform.system() == "Windows":
        return

    # Determine the file extension based on the platform
    lib_ext = ".dylib" if platform.system() == "Darwin" else ".so"
    lib_name = f"libtorch_global_deps{lib_ext}"
    here = os.path.abspath(__file__)
    global_deps_lib_path = os.path.join(os.path.dirname(here), "lib", lib_name)

    try:
        ctypes.CDLL(global_deps_lib_path, mode=ctypes.RTLD_GLOBAL)
        # Workaround slim-wheel CUDA dependency bugs in cusparse and cudnn by preloading nvjitlink
        # and nvrtc. In CUDA-12.4+ cusparse depends on nvjitlink, but does not have rpath when
        # shipped as wheel, which results in OS picking wrong/older version of nvjitlink library
        # if `LD_LIBRARY_PATH` is defined, see https://github.com/pytorch/pytorch/issues/138460
        # Similar issue exist in cudnn that dynamically loads nvrtc, unaware of its relative path.
        # See https://github.com/pytorch/pytorch/issues/145580
        try:
            with open("/proc/self/maps") as f:
                _maps = f.read()

            # libtorch_global_deps.so always depends in cudart, check if its installed and loaded
            if "libcudart.so" not in _maps:
                return
            # If all above-mentioned conditions are met, preload CUDA dependencies
            _preload_cuda_deps()
        except Exception:
            pass

    except OSError as err:
        # Can happen for wheel with cuda libs as PYPI deps
        # As PyTorch is not purelib, but nvidia-*-cu12 is
        _preload_cuda_deps(err)
        ctypes.CDLL(global_deps_lib_path, mode=ctypes.RTLD_GLOBAL)

