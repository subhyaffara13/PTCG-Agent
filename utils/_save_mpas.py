import functools
import os

def _save_mpas(
  gda_manager,
  mpa_targets: list[tuple[MultiprocessArrayType, str]],
  tmp_path: str,
  final_path: str,
  base_path: str,
  keep: int,
  overwrite: bool,
  keep_every_n_steps: int | None,
  ckpt_start_time: float,
  async_manager: AsyncManager | None = None,
):
  """Save the multiprocess arrays given the paths."""
  mpa_list, mpa_subpaths = zip(*mpa_targets)
  mpa_tmp_path, mpa_final_path = (
    tmp_path + MP_ARRAY_POSTFIX,
    final_path + MP_ARRAY_POSTFIX,
  )
  write_commit_success = False
  # If the checkpoint directory is a GCS directory, then keep the final
  # checkpoint directory as the temporary checkpoint directory. This is because
  # renames are not atomic on GCS. When restoring check for the existence of a
  # success file.
  # TODO: figure out a way to unit-test the behavior.
  if tmp_path.startswith('gs://'):
    mpa_tmp_path = mpa_final_path
    write_commit_success = True
  mpa_paths = [os.path.join(mpa_tmp_path, x) for x in mpa_subpaths]
  ts_specs = [get_tensorstore_spec(x) for x in mpa_paths]
  gda_manager.serialize(
    list(mpa_list),
    ts_specs,
    on_commit_callback=functools.partial(
      _save_commit,
      tmp_path,
      final_path,
      base_path,
      keep,
      overwrite,
      keep_every_n_steps,
      ckpt_start_time,
      has_mpa=True,
      write_commit_success=write_commit_success,
      async_manager=async_manager,
    ),
  )

