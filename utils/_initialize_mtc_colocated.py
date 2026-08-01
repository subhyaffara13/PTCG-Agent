
def _initialize_mtc_colocated(
    local_checkpoint_directory: epath.Path,
    backup_interval_minutes: int,
    num_slices: int,
    run_name: str,
    data_parallelism: int,
    timeout_seconds: int,
) -> None:
  """Initializes multi-tier checkpointing with a colocated Python sidecar on all workers.

  Args:
    local_checkpoint_directory: The local checkpoint directory on the
      worker's filesystem.
    backup_interval_minutes: The backup interval in minutes.
    num_slices: The number of slices.
    run_name: The run name.
    data_parallelism: The data parallelism.
    timeout_seconds: The timeout in seconds.
  """
  logging.info(
      'Initializing colocated MTC setup: '
      f'process_count={jax.process_count()}, device_count={jax.device_count()}'
  )
  colocated_transport.install_pathways_colocated_serialization_patch()
  all_devices = jax.devices()

  topology = pathways_topology.Topology.from_devices(tuple(all_devices))
  worker_cpu_devices = topology.worker_cpu_devices()
  worker_rank_in = topology.worker_rank_array(worker_cpu_devices)
  num_nodes = topology.num_workers
  worker_keys = tuple(tuple(worker.key) for worker in topology.workers)
  worker_tpu_device_ids = tuple(
      tuple(int(device_id) for device_id in worker.device_ids)
      for worker in topology.workers
  )
  worker_cpu_device_ids = tuple(int(device.id) for device in worker_cpu_devices)
  peer_ranks_by_worker_rank = tuple(
      tuple(int(rank) for rank in peer_ranks)
      for peer_ranks in topology.peer_ranks_by_worker_rank(num_slices)
  )
  logging.info(
      'Dispatching MTC initialization to %d worker colocated CPU devices '
      'from %d JAX devices.',
      len(worker_cpu_devices),
      len(all_devices),
  )

  dummy_in = dispatchers.get_dummy_input_array(worker_cpu_devices)

  local_dir_str = str(local_checkpoint_directory)

  def _setup(dummy_arg: jax.Array, worker_rank_arg: jax.Array) -> jax.Array:
    """Sets up the initial MTC sidecar and processes restore tasks.

    Args:
      dummy_arg: A dummy JAX array holding dependencies to force order.
      worker_rank_arg: The worker's node rank.

    Returns:
      A JAX array signaling completion, acting as a dependency for further
      setup.
    """
    signaling_client.mark_pathways_colocated_runtime_active()
    deadline = time.time() + timeout_seconds

    def _remaining_timeout_seconds() -> int:
      remaining = int(deadline - time.time())
      if remaining <= 0:
        raise TimeoutError('Timed out while initializing colocated MTC setup.')
      return remaining

    node_rank = pathways_topology.worker_rank_from_array(worker_rank_arg)
    if not 0 <= node_rank < num_nodes:
      raise ValueError(
          f'Invalid node_rank={node_rank} for num_nodes={num_nodes}.'
      )
    worker_key = worker_keys[node_rank]
    tpu_device_ids = worker_tpu_device_ids[node_rank]
    worker_cpu_id = worker_cpu_device_ids[node_rank]
    peer_ranks = list(peer_ranks_by_worker_rank[node_rank])
    loc_dir = epath.Path(local_dir_str)
    logging.vlog(
        2,
        'Pathways MTC worker identity: '
        'logical_worker_rank=%d/%d, worker_key=%s, '
        'tpu_device_ids=%s, worker_cpu_id=%d, peer_ranks=%s, hostname=%s, '
        'kube_node_name=%s, worker_rank_sharding=%s',
        node_rank,
        num_nodes,
        worker_key,
        tpu_device_ids,
        worker_cpu_id,
        peer_ranks,
        os.environ.get('HOSTNAME'),
        os.environ.get('KUBE_NODE_NAME'),
        getattr(worker_rank_arg, 'sharding', None),
    )

    replicator_file = epath.Path(loc_dir) / _REPLICATOR_FILE
    try:
      replicator_file.unlink()
      logging.info('Removed stale replicator.yaml from previous run.')
    except FileNotFoundError:
      pass

    _create_replicator_file(
        loc_dir,
        run_name=run_name,
        num_nodes=num_nodes,
        data_parallelism=data_parallelism,
        node_rank=node_rank,
        peer_ranks=peer_ranks,
        backup_interval_minutes=backup_interval_minutes,
    )
    _wait_for_replicator_file_to_disappear(
        loc_dir,
        timeout_seconds=min(
            _remaining_timeout_seconds(),
            _PATHWAYS_REPLICATOR_FILE_TIMEOUT_SECONDS,
        ),
    )
    _block_and_process_restore_dir(
        loc_dir, timeout_seconds=_remaining_timeout_seconds()
    )

    # Construct a fresh array from local data only.
    return jax.make_array_from_callback(
        dummy_arg.shape,
        dummy_arg.sharding,
        lambda _: np.array(True),
        dtype=jnp.bool_,
    )

  wrapped_setup_fn = colocated_python.colocated_python(_setup)
  wrapped_setup_fn = wrapped_setup_fn.specialize(
      out_specs_fn=lambda dummy_arg, _worker_rank_arg: dummy_arg
  )

  dispatch_start = time.time()
  result = wrapped_setup_fn(dummy_in, worker_rank_in)
  jax.block_until_ready(result)
  logging.info(
      'All shards ready (%.1fs total). Setup complete on all hosts.',
      time.time() - dispatch_start,
  )

