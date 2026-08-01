
def _suggest_missing_backends():
  if py_platform.system() != "Linux":
    # If you're not using Linux (or WSL2), we don't have any suggestions at the
    # moment.
    return

  assert _default_backend is not None
  default_platform = _default_backend.platform
  if "cuda" not in _backends and hardware_utils.has_visible_nvidia_gpu():
    if hasattr(_jax, "GpuAllocatorConfig") and "cuda" in _backend_errors:
      err = _backend_errors["cuda"]
      warning_msg = f"CUDA backend failed to initialize: {err}."
      if "no supported devices found for platform CUDA." in err:
        warning_msg += (
          "This may be due to JAX pre-allocating too much device "
          "memory, leaving too little for CUDA library initialization. See "
          "https://docs.jax.dev/en/latest/gpu_memory_allocation.html "
          "for more details and potential workarounds."
        )
      warning_msg += "(Set TF_CPP_MIN_LOG_LEVEL=0 and rerun for more info.)"

      logger.warning(warning_msg)
    else:
      logger.warning("An NVIDIA GPU may be present on this machine, but a "
                     "CUDA-enabled jaxlib is not installed. Falling back to "
                     f"{default_platform}.")
  elif "tpu" not in _backends and hardware_utils.num_available_tpu_chips_and_device_id()[0] > 0:
    logger.warning("A Google TPU may be present on this machine, but either a "
                    "TPU-enabled jaxlib or libtpu is not installed. Falling "
                    f"back to {default_platform}.")

