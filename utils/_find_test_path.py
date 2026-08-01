
def _find_test_path(test_file_yaml):
  """Returns existing path for test file, or None."""
  if os.path.exists(test_file_yaml):
    return test_file_yaml

  path_suffix = test_file_yaml
  if path_suffix.startswith('//third_party/py/'):
    path_suffix = path_suffix.removeprefix('//third_party/py/')

  if ':' in path_suffix:
    path_suffix = path_suffix.replace(':', '/') + '.py'

  candidate1 = path_suffix
  candidate2 = os.path.join('/app/orbax_repo/checkpoint', path_suffix)
  if os.path.exists(candidate1):
    return candidate1
  elif os.path.exists(candidate2):
    return candidate2
  return None

