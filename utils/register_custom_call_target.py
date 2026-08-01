
def register_custom_call_target(
    name: str,
    fn: Any,
    platform: str = 'cpu',
    api_version: int = 0,
    traits: CustomCallTargetTraits = CustomCallTargetTraits.DEFAULT,
) -> None:
  """Registers a custom call target.

  Args:
    name: bytes containing the name of the function.
    fn: a PyCapsule object containing the function pointer.
    platform: the target platform.
    api_version: the XLA FFI version to use. Supported versions are: 0 for the
      untyped FFI and 1 for the typed FFI.
    traits: custom call traits corresponding to XLA FFI handler traits.
  """
  # To support AMD GPUs, we need to have xla_platform_names["gpu"] == "ROCM"
  # Since that is hardcoded to CUDA, we are using the following as workaround.
  xla_platform_name = xla_platform_names.get(platform, platform)
  with _custom_callback_lock:
    if xla_platform_name in _custom_callback_handler:
      _custom_callback_handler[xla_platform_name](
          name, fn, xla_platform_name, api_version, traits
      )
    else:
      _custom_callback.setdefault(xla_platform_name, []).append(
          (name, fn, api_version, traits)
      )

