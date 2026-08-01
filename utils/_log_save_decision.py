
def _log_save_decision(
    policy_name: str,
    step: PolicyCheckpointInfo,
    is_saving: bool,
) -> None:
  """Logs the save decision."""
  if is_saving:
    logging.vlog(
        1,
        f"{policy_name}: Saving checkpoint at step"
        f" {step.step}).",
    )
  else:
    logging.vlog(
        1,
        f"{policy_name}: Not saving checkpoint at step"
        f" {step.step}).",
    )

