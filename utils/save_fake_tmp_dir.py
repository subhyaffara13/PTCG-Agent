from typing import List, Optional

def save_fake_tmp_dir(
    directory: epath.Path,
    step: int,
    item: str,
    subdirs: Optional[List[str]] = None,
    step_prefix: Optional[str] = None,
) -> epath.Path:
  """Saves a directory with a tmp folder to simulate preemption."""
  subdirs = subdirs or []
  if not step_prefix:
    step_prefix = ''
  step_final_directory = directory / (step_prefix + str(step))
  step_tmp_directory = (
      step_final_directory
      if gcs_utils.is_gcs_path(step_final_directory)
      else atomicity._get_tmp_directory(step_final_directory)
  )
  create_tmp_directory(step_tmp_directory, step_final_directory)

  item_final_directory = step_tmp_directory / item
  item_tmp_directory = (
      item_final_directory
      if gcs_utils.is_gcs_path(item_final_directory)
      else atomicity._get_tmp_directory(item_final_directory)
  )
  create_tmp_directory(item_tmp_directory, item_final_directory)

  if multihost.process_index() == 0:
    for sub in subdirs:
      (item_tmp_directory / sub).mkdir(parents=True)
  sync_global_processes('save_fake_tmp_dir')
  return item_tmp_directory

