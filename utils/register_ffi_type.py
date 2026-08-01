
def register_ffi_type(
    name: str,
    type_registration: TypeRegistration,
    platform: str = "cpu",
) -> None:
  """Registers a custom type for a FFI target.

  Args:
    name: the name of the type. This name must be unique within the process.
    type_registration: a ``TypeRegistration`` defining the external type.
    platform: the target platform.
  """
  return xla_client.register_custom_type(
      name, type_registration, platform=platform
  )

