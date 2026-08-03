from typing import Any

def register_ffi_type_id(
    name: str,
    obj: Any,
    platform: str = "cpu",
) -> None:
  """Registers a custom type ID for a FFI target.

  Args:
    name: the name of the type ID. This name must be unique within the process.
    obj: a ``PyCapsule`` object encapsulating a pointer to the type ID.
    platform: the target platform.
  """
  raise ValueError(
      "register_ffi_type_id is not supported after jaxlib version 381.")

