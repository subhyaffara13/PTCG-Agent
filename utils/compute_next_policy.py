
def compute_next_policy(infostates: List[InfostateNode],
                        cfr_plus: bool = False) -> None:
  """Computes policy of next iteration for each infostate in infostates.

  Args:
    infostates: List of information states.
    cfr_plus: A flag which specifies if we update policy according to CFR or
      CFR-plus algorithm. True if we use CFR-plus, otherwise we use CFR.
  """
  for infostate in infostates:
    infostate_actions = infostate.get_actions()
    if cfr_plus:
      for action in infostate_actions:
        infostate.regret[action] = max(infostate.regret[action], 0.0)

    positive_regret_sum = 0
    for action in infostate_actions:
      if infostate.regret[action] > 0:
        positive_regret_sum += infostate.regret[action]

    actions_count = len(infostate_actions)
    next_policy = {a: 1.0 / actions_count for a in infostate_actions}

    if positive_regret_sum > 0:
      for action in infostate_actions:
        next_policy[action] = max(infostate.regret[action],
                                  0) / positive_regret_sum
    infostate.policy = next_policy


def compute_next_policy(infostates: typing.InfostateMapping,
                        net_apply: typing.ApplyFn, net_params: typing.Params,
                        epoch: int, all_actions: List[int],
                        one_hot_representations: Dict[str, jnp.ndarray],
                        illegal_actions: Dict[str,
                                              List[int]], key: hk.PRNGSequence):
  """Computes next step policy from output of the model.

  Args:
    infostates: List of infostate mappings.
    net_apply: Apply function.
    net_params: Model params.
    epoch: epoch.
    all_actions: List of actions.
    one_hot_representations: Dictionary from infostate string to infostate.
    illegal_actions: Dictionary from infostate string to the list of illegal
      actions.
    key: Haiku Pseudo random number generator.
  """

  infostate_lst = []
  input_lst = []
  illegal_action_lst = []

  batched_net_output = []
  for (infostate_str, infostate) in infostates.items():
    if infostate.is_terminal():
      continue

    legal_actions = infostate.get_actions()
    if len(legal_actions) == 1:
      infostate.policy[infostate.get_actions()[0]] = 1
      continue
    regret_vec = np.array([
        infostate.regret[a] /
        (epoch + 1) if a in infostate.get_actions() else 0
        for a in all_actions
    ])
    if FLAGS.use_infostate_representation:
      one_hot_representation = one_hot_representations[infostate_str]
      net_input = jnp.concatenate([regret_vec, one_hot_representation])
    else:
      net_input = regret_vec
    input_lst.append(net_input)
    infostate_lst.append(infostate)
    illegal_action_lst.append(illegal_actions[infostate_str])
  batched_inputs, output_mappings, relevant_illegal_actions = (
      utils.get_batched_input(
          input_lst, infostate_lst, illegal_action_lst, FLAGS.batch_size
      )
  )
  idx = 0

  for _ in range(int(len(batched_inputs) / FLAGS.batch_size)):
    batched_input, output_mapping, relevant_illegal_action = batched_inputs[
        idx:idx + FLAGS.batch_size], output_mappings[
            idx:idx +
            FLAGS.batch_size], relevant_illegal_actions[idx:idx +
                                                        FLAGS.batch_size]
    idx += FLAGS.batch_size

    batched_input_jnp = jnp.array(
        np.expand_dims(np.array(batched_input), axis=1))
    batched_net_output = utils.get_network_output_batched(  # pytype: disable=wrong-arg-types  # jnp-type
        net_apply, net_params,
        batched_input_jnp,
        relevant_illegal_action, key)
    for i, infostate in enumerate(output_mapping):
      net_output = jnp.squeeze(batched_net_output[i])
      for ai, action in enumerate(infostate.get_actions()):
        infostate.policy[action] = float(net_output[ai])

