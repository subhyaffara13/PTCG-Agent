
def _validate_output_directory(flags_dict):
  out_dir = flags_dict['output_directory']
  storage = flags_dict['storage']
  if storage:
    return True
  return out_dir.startswith('gs://')

