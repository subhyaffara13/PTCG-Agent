
def _compile_as_torch_gpu_kernel(module_asm: bytes):
  try:
    import torch  # pyrefly: ignore[missing-import]
  except ImportError:
    raise RuntimeError("Can't compile for PyTorch: import torch failed") from None

  torch.cuda.init()  # Make sure CUDA context is set up.

  # Get our hands on the compilation and unload functions
  try:
    try:
      import jax_plugins.xla_cuda13 as cuda_plugin  # pyrefly: ignore[missing-import]
    except ImportError:
      import jax_plugins.xla_cuda12 as cuda_plugin  # pyrefly: ignore[missing-import]
  except ImportError:
    dll = ctypes.CDLL(None)
  else:
    dll = ctypes.CDLL(cuda_plugin._get_library_path())
  compile_func = dll.MosaicGpuCompile
  compile_func.argtypes = [ctypes.c_void_p]
  compile_func.restype = ctypes.POINTER(ctypes.c_void_p)
  unload_func = dll.MosaicGpuUnload
  unload_func.argtypes = [compile_func.restype]
  unload_func.restype = None

  compiled = compile_func(ctypes.c_char_p(module_asm), ctypes.c_int(len(module_asm)))
  if not compiled:
    raise RuntimeError("Failed to compile the module")
  ctx, launch_ptr = compiled[0], compiled[1]
  ctx_ptr_ptr = ctypes.pointer(ctypes.c_void_p(ctx))
  launch_c = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(launch_ptr)

  def launch(arg_ptrs, device):
    # Allocate another buffer for args of the host-side program. This is sadly
    # the default MLIR calling convention.
    launch_args_ptr = (ctypes.POINTER(ctypes.c_void_p) * 3)()
    launch_args_ptr[0] = ctx_ptr_ptr
    launch_args_ptr[1] = ctypes.pointer(
        torch.cuda.default_stream(device)._as_parameter_
    )
    launch_args_ptr[2] = ctypes.cast(
        ctypes.pointer(ctypes.pointer(arg_ptrs)),
        ctypes.POINTER(ctypes.c_void_p),
    )
    launch_c(launch_args_ptr)

  return launch, functools.partial(unload_func, compiled)

