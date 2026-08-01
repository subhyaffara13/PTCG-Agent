
def register_custom_type(
    type_name: str,
    type_id: Any,
    platform: str = 'cpu',
) -> None:
  """Register a custom type id for use with the FFI.

  Args:
    type_name: a unique name for the type.
    type_id: a PyCapsule object containing a pointer to the ``ffi::TypeId``.
    platform: the target platform.
  """
  xla_platform_name = xla_platform_names.get(platform, platform)
  with _custom_type_id_lock:
    if xla_platform_name in _custom_type_id_handler:
      _custom_type_id_handler[xla_platform_name](type_name, type_id)
    else:
      _custom_type_id.setdefault(xla_platform_name, []).append(
          (type_name, type_id)
      )

