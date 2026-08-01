
def construct_workload_command(
    *,
    workload_name: str,
    config_file: str,
    output_directory: str,
    run_id: str,
    enable_pathways: bool,
    benchmark_binary_path: str,
    hardware_type: HardwareType,
    v_level: int | None,
) -> str:
  """Constructs the command to run inside the workload."""
  # Environment variables
  if enable_pathways:
    env_vars = [
        'export JAX_PLATFORMS=proxy',
        'export JAX_BACKEND_TARGET=grpc://${PATHWAYS_HEAD}:29000',
        'export ENABLE_PJRT_COMPATIBILITY=true',
    ]
  else:
    if hardware_type == HardwareType.TPU:
      env_vars = ['export JAX_PLATFORMS=tpu,cpu']
    elif hardware_type == HardwareType.GPU:
      env_vars = ['export JAX_PLATFORMS=gpu,cpu']
    elif hardware_type == HardwareType.CPU:
      fqdn_address = f'{workload_name}-slice-job-0-0.{workload_name}.default.svc.cluster.local'
      env_vars = [
          'export JAX_PLATFORMS=cpu',
          'export JAX_NUM_PROCESSES=$JAX_PROCESS_COUNT',
          (
              'export JAX_PROCESS_ID=$(($JOB_INDEX * $PROCESSES_IN_JOB +'
              ' $JOB_COMPLETION_INDEX))'
          ),
          (
              'export JAX_COORDINATOR_ADDRESS=$(if [ "$JAX_PROCESS_ID" = "0" ];'
              f' then echo "localhost"; else echo "{fqdn_address}"; fi):1234'
          ),
          'export XLA_FLAGS="--xla_cpu_collective_timeout_seconds=600"',
          'echo JOB_INDEX = $JOB_INDEX',
          'echo JAX_PROCESS_ID = $JAX_PROCESS_ID',
          'echo JAX_COORDINATOR_ADDRESS = $JAX_COORDINATOR_ADDRESS',
          'echo JAX_NUM_PROCESSES = $JAX_NUM_PROCESSES',
      ]
    else:
      raise ValueError(f'Unsupported hardware type: {hardware_type}')

  env_cmd = ' && '.join(env_vars) + ' && ' if env_vars else ''

  python_args = [
      f'python3 {benchmark_binary_path}',
      f'--config_file={config_file}',
      f'--output_directory={os.path.join(output_directory, run_id)}',
      '--alsologtostderr',
  ]
  if _RAMDISK_DIRECTORY.value is not None:
    python_args.append(f'--local_directory={_RAMDISK_DIRECTORY.value}')
  if v_level is not None:
    python_args.append(f'--v={v_level}')

  python_cmd = ' '.join(python_args)
  if hardware_type == HardwareType.CPU:
    python_cmd += ' --jax_cpu_collectives_implementation=gloo'
  if enable_pathways:
    python_cmd = (
        'python3 -c "import pathwaysutils; pathwaysutils.initialize();'
        " print('Pathwaysutils initialized.')\" && "
        + python_cmd
    )

  return f'{env_cmd}{python_cmd}'

