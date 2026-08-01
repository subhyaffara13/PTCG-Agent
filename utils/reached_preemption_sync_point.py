
def reached_preemption_sync_point(step_id: int) -> bool:
  """Determine whether all hosts have reached a preemption sync step.

  When any host receives a preemption notice, the notice is propagated to all
  hosts and triggers a synchronization protocol in the background. The
  synchronization protocol calculates the maximum step ids from all hosts, and
  uses the next step id (i.e., max + 1) as the safe step to save a checkpoint.
  All hosts should continue training more steps until this method returns True,
  indicating that the `step_id` is equal to the safe step and the hosts should
  start saving a checkpoint.

  To use this API, all hosts must start training from the same step and call it
  at every training step. Example usage:

  ```
  def should_save(step_id: int) -> bool:

    # Should save an on-demand checkpoint for preemption
    if multihost_utils.reached_preemption_sync_point(step_id):
      return True

    # Should save a regular checkpoint
    return step_id - last_saved_checkpoint_step >= save_interval_steps
  ```

  Preemption notice is provided by the cluster scheduler to notify the
  application in advance before it gets evicted. By default, we use SIGTERM as
  the signal for preemption notice.

  TODO(b/230630494): Add instructions for customized preemption notice.

  Returns:
    A boolean indicating whether all hosts have reached a synchronization step
    after some hosts are preempted.

  Raises:
    RuntimeError: if preemption sync manager has not been initialized.
  """
  if distributed.global_state.client is None:
    return False
  sync_manager = distributed.global_state.preemption_sync_manager
  if sync_manager is None:
    raise RuntimeError(
        "Preemption sync manager has not been initialized. Make sure the"
        " 'jax_enable_preemption_service' config is enabled."
    )
  return sync_manager.reached_sync_point(step_id)

