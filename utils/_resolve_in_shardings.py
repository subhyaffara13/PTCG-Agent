
def _resolve_in_shardings(args, pjit_in_shardings: Sequence[PjitSharding]
                          ) -> Sequence[PjitSharding]:
  # If True, means that device or backend is set by the user on pjit and it
  # has the same semantics as device_put i.e. doesn't matter which device the
  # arg is on, reshard it to the device mentioned. So don't do any of the
  # checks and just return the pjit_in_shardings directly. `shard_args` will
  # handle the resharding.
  if pxla.check_device_backend_on_shardings(pjit_in_shardings):
    return pjit_in_shardings

  resolved_in_shardings: list[PjitSharding] = []
  for arg, pjit_in_s in zip(args, pjit_in_shardings):
    # arg sharding can be None in case of ShapeDtypeStruct. jax.Array does
    # not allow None as the sharding.
    arg_s, committed = ((arg.sharding, arg.committed) if arg.sharding is not None
                        else (UNSPECIFIED, False))
    if isinstance(arg_s, NamedSharding) and arg_s.mesh.empty:
      arg_s, committed = UNSPECIFIED, False
    if isinstance(pjit_in_s, UnspecifiedValue):
      resolved_in_shardings.append(finalize_arg_sharding(arg_s, committed))
    else:
      if (arg.is_np_array and not pjit_in_s.is_fully_replicated and
          xb.process_count() > 1):
        raise ValueError(
            'Passing non-trivial shardings for numpy '
            'inputs is not allowed. To fix this error, either specify a '
            'replicated sharding explicitly or use '
            '`jax.make_array_from_process_local_data(...)` '
            'to convert your host local numpy inputs to a jax.Array which you '
            'can pass to jit. '
            'If the numpy input is the same on each process, then you can use '
            '`jax.make_array_from_callback(...) to create a `jax.Array` which '
            f'you can pass to jit. Got arg type: {arg.aval}')
      if not isinstance(arg_s, UnspecifiedValue) and arg_s._is_concrete:
        # jax.jit does not allow resharding across different memory kinds even
        # if the argument is uncommitted. Use jax.device_put for those cases,
        # either outside or inside jax.jit.
        if pjit_in_s.memory_kind != arg_s.memory_kind:
          raise ValueError(
              'Memory kinds passed to jax.jit does not match memory kind on the'
              f' respective arg. Got jit memory kind: {pjit_in_s.memory_kind}, '
              f'arg memory kind: {arg_s.memory_kind} for arg type: {arg.aval}')
        if (committed and
            not op_shardings.are_hlo_shardings_equal(
                pjit_in_s._to_xla_hlo_sharding(arg.ndim),
                arg_s._to_xla_hlo_sharding(arg.ndim))):
          raise ValueError('Sharding passed to jit does not match the sharding '
                           'on the respective arg. '
                           f'Got jit sharding: {pjit_in_s},\n'
                           f'arg sharding: {arg_s} for arg type: {arg.aval}')
      resolved_in_shardings.append(pjit_in_s)

  return tuple(resolved_in_shardings)

