
def construct_xpk_command(
    workload_name: str, workload_command: str
) -> Sequence[str]:
  """Constructs the XPK CLI command."""
  base_cmd = [
      _XPK_PATH.value,
      'workload',
      'create-pathways' if _ENABLE_PATHWAYS.value else 'create',
      f'--cluster={_CLUSTER_NAME.value}',
      f'--project={_PROJECT.value}',
      f'--zone={_ZONE.value}',
      f'--workload={workload_name}',
      f'--num-slices={_NUM_SLICES.value}',
      f'--priority={_PRIORITY.value}',
  ]

  if _STORAGE.value is not None:
    base_cmd.append(f'--storage={_STORAGE.value}')
  if _TPU_TYPE.value is not None:
    base_cmd.append(f'--tpu-type={_TPU_TYPE.value}')
  if _DEVICE_TYPE.value is not None:
    base_cmd.append(f'--device-type={_DEVICE_TYPE.value}')

  if _MAX_RESTARTS.value > 0:
    base_cmd.append(f'--max-restarts={_MAX_RESTARTS.value}')

  # Workload Customization
  if _SCHEDULER.value is not None:
    base_cmd.append(f'--scheduler={_SCHEDULER.value}')
  if _DEBUG_DUMP_GCS.value is not None:
    base_cmd.append(f'--debug-dump-gcs={_DEBUG_DUMP_GCS.value}')
  if _USE_VERTEX_TENSORBOARD.value:
    base_cmd.append('--use-vertex-tensorboard')
  if _EXPERIMENT_NAME.value is not None:
    base_cmd.append(f'--experiment-name={_EXPERIMENT_NAME.value}')
  if _ENV.value:
    for env_var in _ENV.value:
      base_cmd.append(f'--env={env_var}')
  if _ENV_FILE.value is not None:
    base_cmd.append(f'--env-file={_ENV_FILE.value}')
  if _DOCKER_NAME.value is not None:
    base_cmd.append(f'--docker-name={_DOCKER_NAME.value}')
  if _SA.value is not None:
    base_cmd.append(f'--sa={_SA.value}')
  if _RUN_NAME.value is not None:
    base_cmd.append(f'--run-name={_RUN_NAME.value}')
  if _ENABLE_OPS_AGENT.value:
    base_cmd.append('--enable-ops-agent')
  if _RAMDISK_DIRECTORY.value is not None:
    base_cmd.append('--mtc-enabled')
  if _SKIP_VALIDATION.value:
    base_cmd.append('--skip-validation')

  if _ENABLE_PATHWAYS.value:
    if not _PATHWAYS_SERVER_IMAGE.value:
      raise ValueError(
          'Pathways requires --pathways_server_image to be specified.'
      )
    if not _PATHWAYS_PROXY_IMAGE.value:
      raise ValueError(
          'Pathways requires --pathways_proxy_image to be specified.'
      )

    image_args = [
        f'--server-image={_PATHWAYS_SERVER_IMAGE.value}',
        f'--proxy-server-image={_PATHWAYS_PROXY_IMAGE.value}',
        f'--colocated-python-sidecar-image={_PATHWAYS_SIDECAR_IMAGE.value}',
        f'--docker-image={_DOCKER_IMAGE.value}',
        # required for colocated python
        '--custom-pathways-proxy-server-args=--sidecar_name=external',
    ]

  else:
    # Standard mode
    image_args = [f'--docker-image={_DOCKER_IMAGE.value}']

  optional_args = []
  if _RESTART_ON_USER_CODE_FAILURE.value:
    optional_args.append('--restart-on-user-code-failure')
  if _RAMDISK_DIRECTORY.value is not None:
    optional_args.append(f'--ramdisk-directory={_RAMDISK_DIRECTORY.value}')

  return list(itertools.chain(
      base_cmd, image_args, optional_args, ['--command', workload_command]
  ))

