
def update_bucket_csi_driver(mount_csi_driver: bool):
  """Mounts or unmounts the Bucket CSI driver.

  Args:
    mount_csi_driver: If True, applies the CSI driver configuration. If False,
      deletes the CSI driver configuration.
  """
  script_dir = os.path.dirname(os.path.realpath(__file__))
  cpc_yaml_path = os.path.join(script_dir, 'cpc.yaml')
  bucket = _OUTPUT_DIRECTORY.value.split('/')[2]
  if mount_csi_driver:
    run_command(
        [
            'bash',
            '-c',
            f'BUCKET_NAME={bucket} envsubst < {cpc_yaml_path} | kubectl apply'
            ' -f -',
        ],
        suppress_output=not _VERBOSE.value,
    )
  else:
    try:
      configs_str = run_command(
          [
              'kubectl',
              'get',
              'checkpointconfiguration',
              '-o',
              'custom-columns=NAME:.metadata.name,BUCKET:.spec.cloudStorageBucketName',
              '--no-headers',
          ],
          capture_output=True,
          suppress_output=not _VERBOSE.value,
      )
      configs_to_delete = []
      if configs_str:
        for line in configs_str.splitlines():
          parts = line.split()
          if len(parts) == 2 and parts[1] == bucket:
            configs_to_delete.append(parts[0])
      if configs_to_delete:
        Console.print_info(
            f'Deleting CheckpointConfigurations: {", ".join(configs_to_delete)}'
        )
        run_command(
            ['kubectl', 'delete', 'checkpointconfiguration']
            + configs_to_delete,
            suppress_output=not _VERBOSE.value,
        )
    except subprocess.CalledProcessError as e:
      output_str = e.output.decode('utf-8') if e.output else ''
      if 'No resources found' in output_str:
        Console.print_info(
            'No CheckpointConfiguration resources found to delete.'
        )
      else:
        Console.print_warning(
            f'Failed to list CheckpointConfigurations: {output_str}'
        )

