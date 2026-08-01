
def _log_preservation_decision(
    policy_name: str,
    checkpoints: Sequence[PolicyCheckpointInfo],
    should_preserve_list: Sequence[bool],
):
  """Logs preservation decisions."""
  if logging.vlog_is_on(1):
    for i, checkpoint in enumerate(checkpoints):
      if should_preserve_list[i]:
        logging.vlog(
            1,
            f" {policy_name}: Preserving checkpoint at step"
            f" {checkpoint.step}).",
        )
      else:
        logging.vlog(
            1,
            f" {policy_name}: Not preserving checkpoint at step"
            f" {checkpoint.step}).",
        )

