
def _lookahead_update(
    updates: base.Updates,
    sync_next: jax.typing.ArrayLike,  # bool
    params: LookaheadParams,
    slow_step_size: jax.typing.ArrayLike,  # float
) -> LookaheadParams:
  """Returns the updates corresponding to one lookahead step.

  Args:
    updates: Updates returned by the fast optimizer.
    sync_next: Wether fast and slow parameters should be synchronized after the
      fast optimizer step.
    params: Current fast and slow parameters as `LookaheadParams` object.
    slow_step_size: Step size of the slow optimizer.

  Returns:
    The updates for the lookahead parameters.

  References:
    Zhang et al, `Lookahead Optimizer: k steps forward, 1 step back
    <https://arxiv.org/abs/1907.08610>`_, 2019
  """
  # In the paper, lookahead is presented as two nested loops. To write lookahead
  # as optax wrapper, these loops have to be broken into successive updates.
  # This leads to two types of update steps:
  #
  # Non-synchronization steps (sync_next == False):
  # The updates returned by the fast optimizer are used for the fast parameters
  # without change and the slow parameter updates are zero (i.e. fast_updates =
  # updates, slow_updates = 0).
  #
  # Synchronization step (sync_next == True):
  # This consists of two substeps: a last fast optimizer step and the
  # synchronization.
  #   Substep 1 (last fast optimizer step):
  #     last_fast_params = fast_params + updates
  #   Substep 2 (synchronization):
  #     new_slow_params = slow_params + slow_step_size * (
  #                       last_fast_params - slow_params)
  #     new_fast_params = new_slow_params
  #
  #   Merging into a single update step we get the update rules:
  #     slow_updates = slow_step_size * (fast_params + updates - slow_params)
  #     fast_updates = new_slow_params - fast_params = updates - (1 -
  #       slow_step_size) * (fast_params + updates - slow_params)
  #
  # To make the equations jittable, the two types of steps are merged. Defining
  # last_difference = fast_params + updates - slow_params, this yields the
  # following equations which are implemented below:
  #   slow_updates = slow_step_size * sync_next * last_difference
  #   fast_updates = updates - (
  #                  1 - slow_step_size) * sync_next * last_difference
  last_difference = jax.tree.map(
      lambda f, u, s: f + u - s, params.fast, updates, params.slow
  )
  slow_updates = jax.tree.map(
      lambda diff: slow_step_size * sync_next * diff, last_difference
  )
  fast_updates = jax.tree.map(
      lambda up, diff: up - sync_next * (1 - slow_step_size) * diff,
      updates,
      last_difference,
  )

  return LookaheadParams(fast=fast_updates, slow=slow_updates)

