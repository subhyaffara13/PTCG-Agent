import os

def upload_config_to_gcs(local_path: str, gcs_root: str, run_id: str) -> str:
  """Uploads the local config file to GCS and returns the GCS path."""
  if not gcs_root.startswith('gs://'):
    raise ValueError('Config diectory is not a GCS path.')

  filename = os.path.basename(local_path)
  gcs_path = os.path.join(gcs_root, run_id, filename)

  Console.print_info(f'Uploading config to {gcs_path}')
  run_command(
      ['gcloud', 'storage', 'cp', local_path, gcs_path], suppress_output=True
  )
  return gcs_path

