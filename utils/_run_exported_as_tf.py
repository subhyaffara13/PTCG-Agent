import logging
from typing import Any

def _run_exported_as_tf(args_flat_tf: Sequence[TfVal],
                        exported: export.Exported,
                        ) -> Sequence[TfVal]:
  """Runs the `exported` as an XlaCallModule TF op.

  Returns: the flattened tuple of results.
  """
  args_avals = exported.in_avals

  # TF values may be integer types for float0
  def _convert_value(val, aval):
    # Check the shape
    assert all(d_aval == d_val
               for d_aval, d_val in zip(aval.shape, val.shape)
               if core.is_constant_dim(d_aval)), (aval, val)
    conversion_dtype = _to_tf_dtype(aval.dtype)
    if conversion_dtype != aval.dtype:
      return tf.cast(val, conversion_dtype)
    else:
      return val

  args_flat_tf = tuple(map(_convert_value, args_flat_tf, args_avals))

  out_shapes_tf = tuple(
      tuple(d if core.is_constant_dim(d) else None
            for d in out_aval.shape)
      for out_aval in exported.out_avals)

  out_types = tuple(_to_tf_dtype(out_aval.dtype) for out_aval in exported.out_avals)

  kept_args_flat_tf = [atf for i, atf in enumerate(args_flat_tf) if i in exported.module_kept_var_idx]

  version = exported.calling_convention_version

  try:
    get_max_supported_version = tfxla.call_module_maximum_supported_version
  except AttributeError:
    get_max_supported_version = None

  if get_max_supported_version:
    max_supported_version = get_max_supported_version()
  else:
    max_supported_version = 6

  if version > max_supported_version:
    raise NotImplementedError(
      "XlaCallModule from your TensorFlow installation supports up to "
      f"serialization version {max_supported_version} but the serialized "
      f"module needs version {version}. "
      "You should upgrade TensorFlow, e.g., to tf_nightly."
    )

  call_module_attrs: dict[str, Any] = dict(
      version=version,
      Tout=out_types,
      Sout=out_shapes_tf,
      function_list=[
          concrete_fn.function_def.signature.name
          for concrete_fn in _thread_local_state.call_tf_concrete_function_list
      ] if _thread_local_state.call_tf_concrete_function_list is not None else [],
      # We always set has_token_input_output because it requires real tokens
      # for versions less than 9 and is not used starting with version 9.
      has_token_input_output=False
  )

  call_module_attrs["platforms"] = tuple(p.upper() for p in exported.platforms)
  if version >= 6:
    call_module_attrs["disabled_checks"] = tuple(
        str(dc)
        for dc in exported.disabled_safety_checks)
  else:
    if version >= 3:
      if DisabledSafetyCheck.platform() in exported.disabled_safety_checks:
        call_module_attrs["platforms"] = ()  # No platform checking

  if version >= 10:
    call_module_attrs["use_shardy_partitioner"] = (
        config.use_shardy_partitioner.value
    )

  if logging.vlog_is_on(3):
    # We already logged the MLIR module when we exported it.
    logging.vlog(3, "XlaCallModule %s", str(call_module_attrs))

  call_module_attrs["module"] = exported.mlir_module_serialized

  # Apply the shardings on arguments and results for pjit. This is redundant
  # because the mlir_module_text will already contain the shardings, but it
  # makes it easier for tools like the TPU inference converter to see the
  # sharding without digging into the `module` attribute of the `XlaCallModule`
  # op, in the same way as it is done for the legacy jax2tf conversion.
  # Do not apply XlaSharding for REPLICATED, on inputs and outputs.
  # This is an agreed convention, and also improves usability under TF eager.
  # See b/255511660.
  kept_in_shardings = []
  for i in exported.module_kept_var_idx:
    if exported._has_named_shardings:
      in_sharding_hlo = _export.named_to_hlo_sharding(
        exported._in_named_shardings[i],
        exported.in_avals[i])
    else:
      in_sharding_hlo = exported.in_shardings_hlo[i]
    kept_in_shardings.append(in_sharding_hlo)
  args_flat_tf = tuple(
    map(partial(_shard_value,
                skip_replicated_sharding=tf.executing_eagerly()),
        kept_args_flat_tf, kept_in_shardings))
  res = tfxla.call_module(args_flat_tf, **call_module_attrs)
  # TODO(b/278940799): Replace the TF v1 API with public TF2 API.
  # Add the custom call tf.function into the default graph, so those functions
  # will be available during tf.SavedModel.save.
  if _thread_local_state.call_tf_concrete_function_list is not None:
    for concrete_fn in _thread_local_state.call_tf_concrete_function_list:
      tf.compat.v1.get_default_graph()._add_function_recursive(
          concrete_fn._inference_function
      )

  if exported._has_named_shardings:
    out_shardings_hlo = tuple(
      _export.named_to_hlo_sharding(s, a)
      for s, a in zip(exported._out_named_shardings, exported.out_avals))
  else:
    out_shardings_hlo = exported.out_shardings_hlo
  res = list(map(partial(_shard_value,
                         skip_replicated_sharding=tf.executing_eagerly()),
                 res, out_shardings_hlo))
  res = tuple(map(_convert_value, res, exported.out_avals))
  return res

