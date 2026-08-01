
def get_critic_update_fn(
    agent_id: int,
    critic_network: hk.Transformed,
    optimizer: optax.TransformUpdateFn,
    num_minibatches: int = 8,
    gamma: float = 0.99,
) -> UpdateFn:
  """Returns the update function for the critic parameters.

  Args:
      agent_id: The id of the agent that will be updated.
      critic_network: A transformed haiku function.
      optimizer: Optimizer update function.
      num_minibatches: the number of minibatches.
      gamma: the discount factor.

  Returns:
      An update function that takes the current train state together with a
      transition batch and returns the new train state and a dictionary of
      metrics.
  """

  def loss_fn(params, batch: TransitionBatch):
    info_states, rewards = batch.info_state[agent_id], batch.reward[agent_id]
    discounts = jnp.ones_like(rewards) * gamma
    values = critic_network.apply(params, info_states).squeeze()
    v_t = values[:, :-1].reshape(-1)
    v_tp1 = values[:, 1:].reshape(-1)
    r_t = rewards[:, :-1].reshape(-1)
    d_t = discounts[:, 1:].reshape(-1)
    td_error = jax.lax.stop_gradient(r_t + d_t * v_tp1) - v_t
    return jnp.mean(td_error**2)

  def update(train_state: TrainState, batch: TransitionBatch):
    """The critic update function.

    Updates the critic parameters of the train state with the given
    transition batch.
    
    Args:
        train_state: The current train state.
        batch: A transition batch.

    Returns:
        The updated train state with the new critic params and a dictionary
        with the critic loss
    """
    losses = []
    critic_params = train_state.critic_params[agent_id]
    opt_state = train_state.critic_opt_states[agent_id]
    for mini_batch in get_minibatches(batch, num_minibatches):
      loss, grads = jax.value_and_grad(loss_fn)(critic_params, mini_batch)
      updates, opt_state = optimizer(grads, opt_state)
      critic_params = optax.apply_updates(critic_params, updates)
      losses.append(loss)
    train_state = deepcopy(train_state)
    state = TrainState(
        policy_params=train_state.policy_params,
        policy_opt_states=train_state.policy_opt_states,
        critic_params={**train_state.critic_params, agent_id: critic_params},
        critic_opt_states={
            **train_state.critic_opt_states,
            agent_id: opt_state,
        },
    )
    return state, {'loss': jnp.mean(jnp.array(losses))}

  return update

