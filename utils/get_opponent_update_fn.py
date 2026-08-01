
def get_opponent_update_fn(
    agent_id: int,
    policy_network: hk.Transformed,
    optimizer: optax.TransformUpdateFn,
    num_minibatches: int = 1,
) -> UpdateFn:
  """Get the opponent update function."""
  def loss_fn(params, batch: TransitionBatch):
    def loss(p, states, actions):
      log_prob = policy_network.apply(p, states).log_prob(actions)
      return log_prob

    log_probs = vmap(vmap(loss, in_axes=(None, 0, 0)), in_axes=(None, 0, 0))(
        params, batch.info_state[agent_id], batch.action[agent_id]
    )
    return -log_probs.sum(axis=-1).mean()

  def update(
      train_state: TrainState, batch: TransitionBatch
  ) -> typing.Tuple[TrainState, typing.Dict]:
    policy_params = train_state.policy_params[agent_id]
    opt_state = train_state.policy_opt_states[agent_id]
    loss = 0
    for mini_batch in get_minibatches(batch, num_minibatches):
      loss, policy_grads = jax.value_and_grad(loss_fn)(
          policy_params, mini_batch
      )
      updates, opt_state = optimizer(policy_grads, opt_state)
      policy_params = optax.apply_updates(
          train_state.policy_params[agent_id], updates
      )

    train_state = TrainState(
        policy_params={**train_state.policy_params, agent_id: policy_params},
        policy_opt_states={
            **train_state.policy_opt_states,
            agent_id: opt_state,
        },
        critic_params=deepcopy(train_state.critic_params),
        critic_opt_states=deepcopy(train_state.critic_opt_states),
    )
    return train_state, {'loss': loss}

  return update

