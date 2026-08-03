import subprocess

def get_credentials() -> None:
  """Gets credentials for the project."""
  try:
    cmd = [
        'gcloud',
        'container',
        'clusters',
        'get-credentials',
        _CLUSTER_NAME.value,
        '--region',
        _REGION.value
    ]
    run_command(cmd, suppress_output=not _VERBOSE.value)
  except subprocess.CalledProcessError as e:
    print(f'Failed to get cluster credentials: {e}')
    return None

