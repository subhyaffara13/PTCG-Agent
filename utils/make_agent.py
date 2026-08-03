from typing import Tuple

def make_agent(
    key: jax.random.PRNGKey,
    player_id: int,
    env: Environment,
    networks: Tuple[hk.Transformed, hk.Transformed],
) -> OpponentShapingAgent:
  """Creates an opponent shaping agent.

  Args:
      key: A random seed key.
      player_id: The id of the player.
      env: The environment.
      networks: A tuple of policy and critic networks transformed by
        hk.transform.

  Returns:
      An opponent shaping agent instance.
  """
  policy_network, critic_network = networks
  return OpponentShapingAgent(
      player_id=player_id,
      opponent_ids=[1 - player_id],
      seed=key,
      info_state_size=env.observation_spec()['info_state'][player_id],
      num_actions=env.action_spec()['num_actions'][player_id],
      policy=policy_network,
      critic=critic_network,
      batch_size=FLAGS.batch_size,
      num_critic_mini_batches=FLAGS.critic_mini_batches,
      pi_learning_rate=FLAGS.policy_lr,
      opp_policy_learning_rate=FLAGS.opp_policy_lr,
      num_opponent_updates=FLAGS.opp_policy_mini_batches,
      critic_learning_rate=FLAGS.critic_lr,
      opponent_model_learning_rate=FLAGS.opponent_model_learning_rate,
      policy_update_interval=FLAGS.policy_update_interval,
      discount=FLAGS.discount,
      critic_discount=0,  # Predict the imm. reward (for iterated matrix games)
      correction_type=FLAGS.correction_type,
      clip_grad_norm=FLAGS.correction_max_grad_norm,
      use_jit=FLAGS.use_jit,
      n_lookaheads=FLAGS.n_lookaheads,
      env=env,
  )

