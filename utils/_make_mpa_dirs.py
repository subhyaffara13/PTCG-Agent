
def _make_mpa_dirs(
  mpa_targets: list[tuple[MultiprocessArrayType, str]], tmp_path: str
):
  # Temporary array path is not used in GCS.
  if tmp_path.startswith('gs://'):
    return
  mpa_tmp_path = tmp_path + MP_ARRAY_POSTFIX
  # Clean up the previous MPA dir, in case some leftover from last preemption
  # lingers.
  if io.exists(mpa_tmp_path):
    logging.info('Removing outdated MPA temporary files at %s', mpa_tmp_path)
    io.rmtree(mpa_tmp_path)
  _, mpa_subpaths = zip(*mpa_targets)
  for subpath in mpa_subpaths:
    io.makedirs(os.path.join(mpa_tmp_path, subpath))

