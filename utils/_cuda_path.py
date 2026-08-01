
def _cuda_path() -> str | None:
  def _try_cuda_root_environment_variable() -> str | None:
    """Use `CUDA_ROOT` environment variable if set."""
    return os.environ.get('CUDA_ROOT', None)

  def _try_cuda_nvcc_import() -> str | None:
    """Try to import `cuda_nvcc` and get its path directly.

    If the pip package `nvidia-cuda-nvcc-cu11` is installed, it should have
    both of the things XLA looks for in the cuda path, namely `bin/ptxas` and
    `nvvm/libdevice/libdevice.10.bc`.
    """
    try:
      nvcc_module = importlib.import_module('nvidia.cu13')
    except ImportError:
      try:
        nvcc_module = importlib.import_module('nvidia.cuda_nvcc')
      except ImportError:
        return None

    cuda_nvcc_path = None
    if hasattr(nvcc_module, '__file__') and nvcc_module.__file__ is not None:
      cuda_nvcc_path = pathlib.Path(nvcc_module.__file__).parent
    elif hasattr(nvcc_module, '__path__') and nvcc_module.__path__ is not None:
      for path in nvcc_module.__path__:
        if (pathlib.Path(path) / 'bin' / 'ptxas').exists():
          cuda_nvcc_path = pathlib.Path(path)
          break
    else:
      return None

    return str(cuda_nvcc_path)

  def _try_bazel_runfiles() -> str | None:
    """Try to get the path to the cuda installation in bazel runfiles."""
    python_runfiles = os.environ.get('PYTHON_RUNFILES')
    if not python_runfiles:
      return None
    cuda_nvcc_root = os.path.join(python_runfiles, 'cuda_nvcc')
    if os.path.exists(cuda_nvcc_root):
      return cuda_nvcc_root
    return None

  if (path := _try_cuda_root_environment_variable()) is not None:
    return path
  elif (path := _try_cuda_nvcc_import()) is not None:
    return path
  elif (path := _try_bazel_runfiles()) is not None:
    return path

  return None

