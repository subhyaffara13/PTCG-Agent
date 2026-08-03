import json
import logging

def read_process_metadata(directory: epath.Path):
  """Read process metadata from the given path."""
  metadata_folder = process_metadata_folder(directory)
  if not metadata_folder.exists():
    raise FileNotFoundError(
        f'Process metadata folder does not exist at {metadata_folder}. The'
        ' local checkpoint cannot be restored.'
    )
  if step_lib.is_path_temporary(metadata_folder):
    raise ValueError(
        f'Process metadata folder was not finalized at {metadata_folder}.'
        ' The local checkpoint cannot be restored.'
    )
  logging.info('Loading process index metadata from %s', metadata_folder)

  distributed_to_device_ids = json.loads(
      (metadata_folder / _GLOBAL_PROCESS_METADATA_FILE_NAME).read_text()
  )
  device_ids = json.loads(
      (metadata_folder / _MESH_METADATA_FILE_NAME).read_text()
  )
  return distributed_to_device_ids, device_ids

