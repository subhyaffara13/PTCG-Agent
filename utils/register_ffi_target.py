
def register_ffi_target(
    name: str,
    fn: Any,
    platform: str = "cpu",
    api_version: int = 1,
    **kwargs: Any,
) -> None:
  """Registers a foreign function target.

  Args:
    name: the name of the target.
    fn: a ``PyCapsule`` object containing the function pointer, or a ``dict``
      where the keys are FFI stage names (e.g. `"execute"`) and the values are
      ``PyCapsule`` objects containing a pointer to the handler for that stage.
    platform: the target platform.
    api_version: the XLA custom call API version to use. Supported versions are:
      1 (default) for the typed FFI or 0 for the earlier "custom call" API.
    kwargs: any extra keyword arguments are passed directly to
      :func:`~jaxlib.xla_client.register_custom_call_target` for more advanced
      use cases.
  """
  return xla_client.register_custom_call_target(name, fn, platform, api_version,
                                                **kwargs)

