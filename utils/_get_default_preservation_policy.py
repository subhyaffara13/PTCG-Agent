
def _get_default_preservation_policy(
    options: CheckpointManagerOptions,
) -> preservation_policy_lib.PreservationPolicy:
  """Returns a default preservation policy."""
  preservation_policies = []
  if options.keep_period is not None:
    preservation_policies.append(
        preservation_policy_lib.EveryNSteps(options.keep_period)
    )
  if options.keep_time_interval is not None:
    total_seconds = int(options.keep_time_interval.total_seconds())
    preservation_policies.append(
        preservation_policy_lib.EveryNSeconds(interval_secs=total_seconds)
    )
  if options.best_fn is not None:
    preservation_policies.append(
        preservation_policy_lib.BestN(
            get_metric_fn=options.best_fn,
            reverse=(options.best_mode == 'min'),
            n=options.max_to_keep,
            keep_checkpoints_without_metrics=options.keep_checkpoints_without_metrics,
        )
    )
  else:
    preservation_policies.append(
        preservation_policy_lib.LatestN(n=options.max_to_keep)
    )
  return preservation_policy_lib.AnyPreservationPolicy(preservation_policies)

