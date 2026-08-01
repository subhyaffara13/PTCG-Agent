
def lookup_ndarray_adapter(
    possible_array: Any,
) -> ndarray_adapters.NDArrayAdapter[Any] | None:
  """Looks up an NDArray adapter for the given type.

  This function looks for an NDArray adapter by first checking for the
  `__treescope_ndarray_adapter__` method on the type, and then by looking up
  the type in the global registry `NDARRAY_ADAPTER_REGISTRY`.

  Args:
    possible_array: The object to look up an adapter for.

  Returns:
    An NDArray adapter for the given type, or None if no adapter was found.
  """
  has_adapter_method = object_inspection.safely_get_real_method(
      possible_array, "__treescope_ndarray_adapter__"
  )
  if has_adapter_method:
    return has_adapter_method()
  else:
    return _lookup_by_mro(NDARRAY_ADAPTER_REGISTRY, type(possible_array))

