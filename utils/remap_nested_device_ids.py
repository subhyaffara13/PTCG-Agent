
def remap_nested_device_ids(
    nested_device_ids: Sequence[Sequence[int]],
    source_device_ids: Sequence[int],
    target_device_ids: Sequence[int],
    *,
    nested_device_ids_name: str,
    source_device_ids_name: str,
    target_device_ids_name: str,
) -> tuple[tuple[int, ...], ...]:
  """Remaps nested device ids from a source namespace to a target namespace."""
  if len(source_device_ids) != len(target_device_ids):
    raise ValueError(
        f'{source_device_ids_name} and {target_device_ids_name} must have the '
        f'same length, got {len(source_device_ids)} and '
        f'{len(target_device_ids)}.'
    )
  target_id_by_source_id = {
      int(source_id): int(target_id)
      for source_id, target_id in zip(source_device_ids, target_device_ids)
  }
  missing_source_ids = {  # pylint: disable=g-complex-comprehension
      int(device_id)
      for device_ids in nested_device_ids
      for device_id in device_ids
      if int(device_id) not in target_id_by_source_id
  }
  if missing_source_ids:
    raise ValueError(
        f'{nested_device_ids_name} contains device ids not present in '
        f'{source_device_ids_name}: {sorted(missing_source_ids)}.'
    )
  return tuple(
      tuple(target_id_by_source_id[int(device_id)] for device_id in device_ids)
      for device_ids in nested_device_ids
  )

