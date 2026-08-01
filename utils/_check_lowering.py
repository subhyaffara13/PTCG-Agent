
def _check_lowering(lowering) -> None:
  if not isinstance(lowering, pxla.MeshComputation):
    raise NotImplementedError(f"serialization is supported only for jit. {lowering}")

  if lowering.compile_args["host_callbacks"] or lowering.compile_args["keepalive"]:
    raise NotImplementedError("serialization of host_callbacks is not yet implemented")
  # Check that we do not see new compile_args. When we add a compile_args it is
  # safe to add it to the allowed_compile_args if it does not change the semantics
  # or the calling convention of the lowered module.
  allowed_compile_args = {
      "backend", "platforms", "mesh", "global_in_avals",
      "global_out_avals", "in_shardings", "out_shardings", "kept_var_idx",
      "mut", "auto_spmd_lowering",
      "tuple_args", "ordered_effects", "unordered_effects",
      "keepalive", "host_callbacks", "committed",
      "device_assignment", "jaxpr_debug_info", "shape_poly_state",
      "all_default_mem_kind", "in_layouts", "out_layouts", "all_args_info",
      "pgle_profiler", "intermediate_shardings", "context_mesh",
      "num_devices"}
  for compile_arg in lowering.compile_args.keys():
    if compile_arg not in allowed_compile_args:
      raise NotImplementedError(f"Unrecognized lowered.compile_args[{compile_arg}]")

  # We have not implemented support for some of the compile_args. Check here that
  # the compile_args have the values that have been implemented.
  not_implemented_msgs = []
  for compile_arg, check_value, err_msg in (
      ("auto_spmd_lowering", lambda v: not v, "False"),
      # tuple_args is a compilation flag, does not affect lowering.
      ("tuple_args", lambda v: True, "N/A"),
      # unordered_effects do not change the calling convention. Those from
      # jax.debug will also result in keepalive being non-empty and unsupported
      # custom calls. The CallTfEffect is an exception, but we want to allow
      # that one.
      ("unordered_effects", lambda v: True, "N/A"),
      ("ordered_effects", lambda v: True, "N/A"),
      # used for TPU jax.debug, send/recv. Not supported yet.
      ("host_callbacks", lambda v: not v, "empty"),
      # used on all platforms for callbacks. Not supported yet.
      ("keepalive", lambda v: not v, "empty"),

      ("shape_poly_state", lambda v: True, "N/A"),
  ):
    if compile_arg in lowering.compile_args:
      if not check_value(lowering.compile_args[compile_arg]):
        not_implemented_msgs.append(
            f"{compile_arg} must be {err_msg} and it is {lowering.compile_args[compile_arg]}")
  if not_implemented_msgs:
    raise NotImplementedError(
        "serialization error, unimplemented lowered.compile_args:\n" +
        "\n".join(not_implemented_msgs))

