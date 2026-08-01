
def make_cpu_client(
    asynchronous=True,
    distributed_client=None,
    node_id=0,
    num_nodes=1,
    collectives=None,
    num_devices=None,
    get_local_topology_timeout_minutes=None,
    get_global_topology_timeout_minutes=None,
    transfer_server_factory=None,
) -> Client:
  register_custom_call_handler('cpu', _xla.register_custom_call_target)
  register_custom_type_handler('cpu', _xla.register_custom_type)
  return _xla.get_tfrt_cpu_client(
      asynchronous=asynchronous,
      distributed_client=distributed_client,
      node_id=node_id,
      num_nodes=num_nodes,
      collectives=collectives,
      num_devices=num_devices,
      get_local_topology_timeout_minutes=get_local_topology_timeout_minutes,
      get_global_topology_timeout_minutes=get_global_topology_timeout_minutes,
      transfer_server_factory=transfer_server_factory,
  )


def make_cpu_client(
    collectives: _jax.CpuCollectives | None = None,
) -> xla_client.Client:
  """Creates a CPU client with the requested collectives implementation.

  The implementation of CPU collectives used by the client is determined by the
  flag `--jax_cpu_collectives_implementation` - unless `collectives` is
  provided, in which case the flag is overridden and `collectives` is used.

  Args:
    collectives: An optional CPU collectives implementation, used by the client
      if provided.

  Raises:
    RuntimeError: If `--jax_cpu_collectives_implementation` is unknown.

  Returns:
    The created CPU client.
  """
  # TODO(skyewm): use distributed.is_initialized() after
  # https://github.com/jax-ml/jax/pull/26172 goes in.
  if collectives is None and distributed.global_state.client is not None:
    collectives_impl = config.cpu_collectives_implementation.value
    if collectives_impl == 'gloo':
      collectives = _jax.make_gloo_tcp_collectives(
        distributed_client=distributed.global_state.client,
      )
    elif collectives_impl == 'mpi':
      collectives = _jax.make_mpi_collectives()
      collectives.Init()
      atexit.register(collectives.Finalize)
    else:
      # Already validated by config module
      assert collectives_impl is None

  num_devices = num_cpu_devices.value if num_cpu_devices.value >= 0 else None
  return xla_client.make_cpu_client(
      asynchronous=_CPU_ENABLE_ASYNC_DISPATCH.value,
      distributed_client=distributed.global_state.client,
      node_id=distributed.global_state.process_id,
      num_nodes=distributed.global_state.num_processes,
      collectives=collectives,
      num_devices=num_devices,
      get_local_topology_timeout_minutes=cpu_get_local_topology_timeout_minutes.value,
      get_global_topology_timeout_minutes=cpu_get_global_topology_timeout_minutes.value,
      transfer_server_factory=_make_transfer_server_factory(),
  )

