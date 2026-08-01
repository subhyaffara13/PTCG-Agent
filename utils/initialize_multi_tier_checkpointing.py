
def initialize_multi_tier_checkpointing(
    local_checkpoint_directory: epath.Path,
    *,
    backup_interval_minutes: int = 30,
    num_slices: Optional[int] = None,
    run_name: Optional[str] = None,
    data_parallelism: Optional[int] = None,
    jax_initialization_timeout_seconds: int = 900,
    use_mtc_process_ids: bool = True,
    use_colocated_python: bool = False,
):
  """Initializes multi-tier checkpointing.

  Args:
    local_checkpoint_directory: The local checkpoint directory.
    backup_interval_minutes: The backup interval for the replicator service, in
      minutes.
    num_slices: The number of slices.
    run_name: The name of the run.
    data_parallelism: Number of identical pipelines in job, should be
      equal to ICI data parallelism * DCN data parallelism. If not provided, it
      will be inferred from the number of slices.
    jax_initialization_timeout_seconds: The timeout for JAX initialization.
    use_mtc_process_ids: Use the MTC rank server to calculate process ids.
    use_colocated_python: Whether to use Colocated Python for initialization.
  """
  run_name = run_name if run_name else os.environ.get('JOBSET_NAME')
  if not run_name:
    raise ValueError(
        'Run name is not set and JOBSET_NAME is not set in the environment.'
    )

  if use_colocated_python:
    num_slices = num_slices or multislice.slice_count()
    data_parallelism = data_parallelism or num_slices
    logging.info(
        'Initializing multi-tier checkpointing via Colocated Python: '
        f'run_name={run_name}, num_slices={num_slices}, '
        f'data_parallelism={data_parallelism}.'
    )
    _initialize_mtc_colocated(
        local_checkpoint_directory=local_checkpoint_directory,
        backup_interval_minutes=backup_interval_minutes,
        num_slices=num_slices,
        run_name=run_name,
        data_parallelism=data_parallelism,
        timeout_seconds=jax_initialization_timeout_seconds,
    )
    return

  # Standard Multi-Controller Path
  if use_mtc_process_ids:
    process_id = _initialize_jax_from_mtc(
        local_checkpoint_directory, jax_initialization_timeout_seconds
    )
  else:
    process_id = None
    jax.distributed.initialize(
        initialization_timeout=jax_initialization_timeout_seconds,
    )

  num_slices = num_slices or multislice.slice_count()
  data_parallelism = data_parallelism or num_slices
  logging.info(
      'Initializing multi-tier checkpointing: '
      f'run_name={run_name}, num_slices={num_slices}, '
      f'data_parallelism={data_parallelism}.'
  )

  multihost.initialize_runtime_to_distributed_ids()
  multihost.initialize_distributed_to_device_ids()
  _wait_for_replicator_file_to_disappear(
      local_checkpoint_directory,
      timeout_seconds=jax_initialization_timeout_seconds,
  )
  num_nodes = jax.process_count()
  if num_nodes % num_slices != 0:
    raise ValueError(
        'num_nodes must be divisible by num_slices, got '
        f'num_nodes={num_nodes}, num_slices={num_slices}.'
    )
  nodes_per_slice = num_nodes // num_slices
  my_process_index = jax.process_index()
  if not 0 <= my_process_index < num_nodes:
    raise ValueError(
        f'Invalid ProcessIndex={my_process_index} for num_nodes={num_nodes}.'
    )
  node_rank_by_process_index = multihost.runtime_to_distributed_ids()
  _validate_node_rank_by_process_index(
      node_rank_by_process_index, num_nodes=num_nodes
  )
  node_rank = node_rank_by_process_index[my_process_index]
  jax_process_id = (
      jax._src.distributed.global_state.process_id  # pylint: disable=protected-access
  )
  if use_mtc_process_ids:
    logging.vlog(
        1,
        f'Mapping of IDs: jax-init-info.txt={process_id}, '
        f'JaxProcessId={jax_process_id}, NodeRank={node_rank}, '
        f'ProcessIndex={my_process_index}, '
        f'ProcessIndex->NodeRank={node_rank_by_process_index}',
    )
  else:
    logging.vlog(
        1,
        'Mapping of IDs (jax-init-info not used): '
        f'JaxProcessId={jax_process_id}, NodeRank={node_rank}, '
        f'ProcessIndex={my_process_index}, '
        f'ProcessIndex->NodeRank={node_rank_by_process_index}',
    )

  my_in_pipeline_index = my_process_index % nodes_per_slice
  peer_ranks = []
  for i in range(num_slices):
    peer_process_index = i * nodes_per_slice + my_in_pipeline_index
    if peer_process_index != my_process_index:
      peer_process_rank = node_rank_by_process_index[peer_process_index]
      peer_ranks.append(peer_process_rank)
  logging.vlog(1, 'Peers for NodeRank %s: %s', node_rank, peer_ranks)

  _create_replicator_file(
      local_checkpoint_directory,
      run_name=run_name,
      num_nodes=num_nodes,
      data_parallelism=data_parallelism,
      node_rank=node_rank,
      peer_ranks=peer_ranks,
      backup_interval_minutes=backup_interval_minutes,
  )
  _wait_for_replicator_file_to_disappear(
      local_checkpoint_directory,
      timeout_seconds=jax_initialization_timeout_seconds,
  )
  _block_and_process_restore_dir(local_checkpoint_directory)

