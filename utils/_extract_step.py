
def _extract_step(f: str) -> str:
  """Extracts the checkpoint step from an MTC restore file name."""
  match = _RESTORE_DIR_RE.fullmatch(f)
  if match is None:
    raise ValueError(
        'Unexpected restore artifact name. Expected '
        '{job_name}-s{step}-n{node_rank}-w{worker_rank}.restore, got '
        f'{f!r}.'
    )
  return match.group('step')

