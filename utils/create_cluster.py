
def create_cluster() -> None:
  """Creates the XPK cluster."""
  Console.print_info(f'Creating cluster {_CLUSTER_NAME.value}...')

  cmd = [
      _XPK_PATH.value,
      'cluster',
      'create-pathways' if _ENABLE_PATHWAYS.value else 'create',
      f'--cluster={_CLUSTER_NAME.value}',
      f'--project={_PROJECT.value}',
      f'--zone={_ZONE.value}',
      f'--num-slices={_NUM_SLICES.value}',
  ]

  if _TPU_TYPE.value is not None:
    cmd.append(f'--tpu-type={_TPU_TYPE.value}')
  if _DEVICE_TYPE.value is not None:
    cmd.append(f'--device-type={_DEVICE_TYPE.value}')

  # Capacity Type
  if _RESERVATION.value is not None:
    cmd.append(f'--reservation={_RESERVATION.value}')
  elif _ON_DEMAND.value:
    cmd.append('--on-demand')
  elif _SPOT.value:
    cmd.append('--spot')

  # Custom Args
  if _CUSTOM_CLUSTER_ARGUMENTS.value is not None:
    cmd.append(f'--custom-cluster-arguments={_CUSTOM_CLUSTER_ARGUMENTS.value}')
  if _ENABLE_TPU_AUTOLOCK.value:
    cmd.append('--enable-tpu-autolock')
  if _CPU_LIMIT.value is not None:
    cmd.append(f'--cpu-limit={_CPU_LIMIT.value}')
  if _MEMORY_LIMIT.value is not None:
    cmd.append(f'--memory-limit={_MEMORY_LIMIT.value}')

  # Private Cluster
  if _PRIVATE.value:
    cmd.append('--private')
  if _AUTHORIZED_NETWORKS.value:
    cmd.append('--authorized-networks')
    cmd.extend(_AUTHORIZED_NETWORKS.value)

  # Vertex AI Tensorboard
  if _CREATE_VERTEX_TENSORBOARD.value:
    cmd.append('--create-vertex-tensorboard')
  if _TENSORBOARD_REGION.value is not None:
    cmd.append(f'--tensorboard-region={_TENSORBOARD_REGION.value}')
  if _TENSORBOARD_NAME.value is not None:
    cmd.append(f'--tensorboard-name={_TENSORBOARD_NAME.value}')

  if _STORAGE.value and 'lustre' in _STORAGE.value:
    cmd.append('--enable-lustre-csi-driver')
    cmd.append('--enable-legacy-lustre-port')

  # MTC Args
  # We are using MTC to enable ramdisk functionality via GCSFuse, which is
  # required for some benchmarks. We do not use multi-tier checkpointing
  # features of MTC in our testing. Enabling MTC requires specific addons
  # (HighScaleCheckpointing, GcsFuseCsiDriver) and workload-pool for
  # authentication during cluster creation. An alternative approach to enable
  # ramdisk without MTC might be possible and could be explored later.
  if _RAMDISK_DIRECTORY.value:
    if not _OUTPUT_DIRECTORY.value.startswith('gs://'):
      raise ValueError(
          '--ramdisk_directory requires --output_directory to be a gs:// path'
          ' for MTC.'
      )
    bucket = _OUTPUT_DIRECTORY.value.split('/')[2]
    cmd.append('--enable-mtc')
    cmd.append('--mtc-ramdisk-size=32G')
    cmd.append(f'--mtc-gcs-bucket={bucket}')
    cmd.append(
        '--custom-cluster-arguments=--workload-pool=orbax-checkpoint.svc.id.goog'
        ' --addons=HighScaleCheckpointing,GcsFuseCsiDriver'
    )

  run_command(cmd, suppress_output=not _VERBOSE.value)
  Console.print_success(f'Cluster {_CLUSTER_NAME.value} created.')

