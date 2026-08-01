
def get_dice_update_fn(
    agent_id: int,
    rng: hk.PRNGSequence,
    policy_network: hk.Transformed,
    critic_network: hk.Transformed,
    optimizer: optax.TransformUpdateFn,
    opp_pi_lr: float,
    env: rl_environment.Environment,
    n_lookaheads: int = 1,
    gamma: float = 0.99,
):
  """Get the DiCE update function."""
  def magic_box(x):
    return jnp.exp(x - jax.lax.stop_gradient(x))

  @jax.jit
  @partial(jax.vmap, in_axes=(None, 0, 0))
  def get_action(params, s, rng_key):
    pi = policy_network.apply(params, s)
    action = pi.sample(seed=rng_key)
    return action

  def rollout(params, other_params):
    states, rewards, actions = [], [], []
    step = env.reset()
    batch_size = (
        step.observations['batch_size']
        if 'batch_size' in step.observations
        else 1
    )
    while not step.last():
      obs = step.observations
      s_1, s_2 = jnp.array(obs['info_state'][0]), jnp.array(
          obs['info_state'][1]
      )
      if batch_size == 1:
        s_1, s_2 = s_1[None, :], s_2[None, :]
      a_1 = get_action(params, s_1, jax.random.split(next(rng), num=batch_size))
      a_2 = get_action(
          other_params, s_2, jax.random.split(next(rng), num=batch_size)
      )
      a = jnp.stack([a_1, a_2], axis=1)
      step = env.step(a.squeeze())
      r_1, r_2 = jnp.array(step.rewards[0]), jnp.array(step.rewards[1])
      if batch_size == 1:
        r_1, r_2 = r_1[None], r_2[None]
      actions.append(a.T)
      states.append(jnp.stack([s_1, s_2], axis=0))
      rewards.append(jnp.stack([r_1, r_2], axis=0))
    return {
        'states': jnp.stack(states, axis=2),
        'rewards': jnp.stack(rewards, axis=2),
        'actions': jnp.stack(actions, axis=2),
    }

  def dice_correction(train_state: TrainState):
    """Computes the dice update for the given train state.

    Args:
        train_state: The current train state.

    Returns:
        The updated train state with the new policy params and metrics dict.
    """

    @jax.jit
    def dice_objective(params, other_params, states, actions, rewards, values):
      self_logprobs = vmap(
          vmap(lambda s, a: policy_network.apply(params, s).log_prob(a))
      )(states[0], actions[0])
      other_logprobs = vmap(
          vmap(lambda s, a: policy_network.apply(other_params, s).log_prob(a))
      )(states[1], actions[1])
      # apply discount:
      cum_discount = jnp.cumprod(gamma * jnp.ones_like(rewards), axis=1) / gamma
      discounted_rewards = rewards * cum_discount
      discounted_values = values.squeeze() * cum_discount

      # stochastics nodes involved in rewards dependencies:
      dependencies = jnp.cumsum(self_logprobs + other_logprobs, axis=1)
      # logprob of each stochastic nodes:
      stochastic_nodes = self_logprobs + other_logprobs
      # dice objective:
      dice_objective = jnp.mean(
          jnp.sum(magic_box(dependencies) * discounted_rewards, axis=1)
      )
      baseline_term = jnp.mean(
          jnp.sum((1 - magic_box(stochastic_nodes)) * discounted_values, axis=1)
      )
      dice_objective = dice_objective + baseline_term
      return -dice_objective  # want to minimize -objective

    def outer_update(params, opp_params, agent_id, opp_id):
      other_theta = opp_params
      for _ in range(n_lookaheads):
        trajectories = rollout(other_theta, params)
        other_grad = jax.grad(dice_objective)(
            other_theta,
            other_params=params,
            states=trajectories['states'],
            actions=trajectories['actions'],
            rewards=trajectories['rewards'][0],
            values=critic_network.apply(
                train_state.critic_params[opp_id], trajectories['states'][0]
            ),
        )
        # Update the other player's policy:
        other_theta = jax.tree_util.tree_map(
            lambda param, grad: param - opp_pi_lr * grad,
            other_theta,
            other_grad,
        )

      trajectories = rollout(params, other_theta)
      values = critic_network.apply(
          train_state.critic_params[agent_id], trajectories['states'][0]
      )
      loss = dice_objective(
          params=params,
          other_params=other_theta,
          states=trajectories['states'],
          actions=trajectories['actions'],
          rewards=trajectories['rewards'][0],
          values=values,
      )
      return loss, {'loss': loss}

    opp = 1 - agent_id
    grads, metrics = grad(outer_update, has_aux=True)(
        train_state.policy_params[agent_id],
        opp_params=train_state.policy_params[opp],
        agent_id=agent_id,
        opp_id=opp,
    )
    return grads, metrics

  def update(
      train_state: TrainState, batch: TransitionBatch
  ) -> typing.Tuple[TrainState, typing.Dict]:
    """Updates the policy parameters in train_state.

    If lola_weight > 0, the correction term according to Foerster et al. will be
    applied.

    Args:
        train_state: the agent's train state.
        batch: a transition batch

    Returns:
        A tuple (new_train_state, metrics)
    """
    del batch
    grads, metrics = dice_correction(train_state)
    updates, opt_state = optimizer(
        grads, train_state.policy_opt_states[agent_id]
    )
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
    return train_state, metrics

  return update

