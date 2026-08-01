
def _get_default_save_decision_policy(
    options: CheckpointManagerOptions,
) -> save_decision_policy_lib.SaveDecisionPolicy:
  """Creates a default policy from CheckpointManagerOptions."""
  save_interval_policies = []
  if options.should_save_fn is not None:
    save_interval_policies.append(_ShouldSaveFnPolicy(options.should_save_fn))
    save_interval_policies.append(
        save_decision_policy_lib.PreemptionCheckpointingPolicy()
    )
  else:
    if options.save_interval_steps is not None:
      save_interval_policies.append(
          save_decision_policy_lib.FixedIntervalPolicy(
              options.save_interval_steps
          )
      )
    if options.save_on_steps is not None:
      save_interval_policies.append(
          save_decision_policy_lib.SpecificStepsPolicy(options.save_on_steps)
      )
    save_interval_policies.append(
        save_decision_policy_lib.PreemptionCheckpointingPolicy()
    )
    save_interval_policies.append(save_decision_policy_lib.InitialSavePolicy())
  return save_decision_policy_lib.AnySavePolicy(save_interval_policies)

