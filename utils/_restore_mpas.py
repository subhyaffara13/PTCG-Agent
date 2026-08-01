
def _restore_mpas(
  state_dict,
  target: Any | None,
  ckpt_path: str,
  step: int | float | None,
  gda_manager: GlobalAsyncCheckpointManager | None,
  allow_partial: bool = False,
):
  """Restore the multiprocess arrays given the target structure and type."""

  def _check_mpa_errors():
    if not gda_manager:
      raise errors.MPACheckpointingRequiredError(ckpt_path, step)
    if not target and not allow_partial:
      raise errors.MPARestoreTargetRequiredError(ckpt_path, step)

  def _safe_deserialize(
    target_mpas: list[tuple[tuple[Any, ...], MultiprocessArrayType, str]],
    gda_manager: Any,
  ) -> list[MultiprocessArrayType]:
    gda_manager.wait_until_finished()

    # Check if reading from GCS and the array dir is potentially corrupted.
    if ckpt_path.startswith('gs://') and not io.exists(
      os.path.join(ckpt_path + MP_ARRAY_POSTFIX, COMMIT_SUCCESS_FILE)
    ):
      raise errors.MPARestoreDataCorruptedError(step, ckpt_path)

    # Check if the given target array types are valid.
    shardings = []
    for _, arr, path in target_mpas:
      if isinstance(arr, jax.Array):
        shardings.append(arr.sharding)

    # Restore the arrays.
    ts_specs = [get_tensorstore_spec(path) for _, _, path in target_mpas]
    return gda_manager.deserialize(shardings, ts_specs)

  # When target is a single leaf instead of a pytree dict.
  if not isinstance(state_dict, (core.FrozenDict, dict)):
    if (
      _is_multiprocess_array(target)
      and isinstance(state_dict, str)
      and state_dict.startswith(MP_ARRAY_PH)
    ):
      _check_mpa_errors()
      return _safe_deserialize(
        [((), target, ckpt_path + MP_ARRAY_POSTFIX)], gda_manager
      )[0]
    return state_dict

  # Go through the restored checkpoint pytree for all MPAs
  flattened = traverse_util.flatten_dict(state_dict, keep_empty_nodes=True)
  target_flattened = {}
  if target:
    target_flattened = traverse_util.flatten_dict(
      serialization.to_state_dict(target), keep_empty_nodes=True
    )
  # A list of (state_dict_key, target_array, array_file_path) for every array
  # to be restored
  target_mpas = []
  for key, value in flattened.items():
    if isinstance(value, str) and value.startswith(MP_ARRAY_PH):
      _check_mpa_errors()
      if (
        not target
        or (key not in target_flattened)
        or (not _is_multiprocess_array(target_flattened[key]))
      ):
        if allow_partial:
          logging.warning(
            'Multiprocess array %s could not be restored because a valid'
            ' array is not found in target at the corresponding location.'
            ' Proceed to restore other arrays because'
            ' allow_partial_restoration=True',
            key,
          )
        else:
          raise errors.MPARestoreTargetRequiredError(ckpt_path, step, key)
      else:
        mpa_path = os.path.join(
          ckpt_path + MP_ARRAY_POSTFIX, value[len(MP_ARRAY_PH) :]
        )
        target_mpas.append((key, target_flattened[key], mpa_path))

  # If any MPA needs to be restored, call deserialize
  if target_mpas:
    mpa_list = _safe_deserialize(target_mpas, gda_manager)
    for mpa, (key, _, _) in zip(mpa_list, target_mpas):
      flattened[key] = mpa
    state_dict = traverse_util.unflatten_dict(flattened)
  return state_dict

