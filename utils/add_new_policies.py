
def add_new_policies(
    per_player_new_policies,
    per_player_gaps,
    per_player_repeats,
    per_player_policies,
    joint_policies,
    joint_returns,
    game,
    br_selection):
  """Adds novel policies from new policies."""
  num_players = len(per_player_new_policies)
  per_player_num_novel_policies = [0 for _ in range(num_players)]

  # Update policies and policy counts.
  for player in range(num_players):
    new_policies = per_player_new_policies[player]
    new_gaps = per_player_gaps[player]

    repeat_policies = []
    repeat_gaps = []
    repeat_ids = []
    novel_policies = []
    novel_gaps = []
    for new_policy, new_gap in zip(new_policies, new_gaps):
      for policy_id, policy_ in enumerate(per_player_policies[player]):
        if np.all(  # New policy is not novel.
            new_policy.action_probability_array ==
            policy_.action_probability_array):  # pytype: disable=attribute-error  # py39-upgrade
          logging.debug("Player %d's new policy is not novel.", player)
          repeat_policies.append(new_policy)
          repeat_gaps.append(new_gap)
          repeat_ids.append(policy_id)
          break
      else:  # New policy is novel.
        logging.debug("Player %d's new policy is novel.", player)
        novel_policies.append(new_policy)
        novel_gaps.append(new_gap)

    add_novel_policies = []
    add_repeat_ids = []
    if (novel_policies or repeat_policies):
      if br_selection == "all":
        add_novel_policies.extend(novel_policies)
        add_repeat_ids.extend(repeat_ids)
      elif br_selection == "all_novel":
        add_novel_policies.extend(novel_policies)
      elif br_selection == "random":
        index = np.random.randint(0, len(repeat_policies) + len(novel_policies))
        if index < len(novel_policies):
          add_novel_policies.append(novel_policies[index])
        else:
          add_repeat_ids.append(repeat_ids[index - len(novel_policies)])
      elif br_selection == "random_novel":
        if novel_policies:
          index = np.random.randint(0, len(novel_policies))
          add_novel_policies.append(novel_policies[index])
        else:  # Fall back on random.
          index = np.random.randint(0, len(repeat_policies))
          add_repeat_ids.append(repeat_ids[index])
      elif br_selection == "largest_gap":
        if novel_policies:
          index = np.argmax(novel_gaps)
          if novel_gaps[index] == 0.0:  # Fall back to random when zero.
            index = np.random.randint(0, len(novel_policies))
          add_novel_policies.append(novel_policies[index])
        else:  # Fall back on random.
          index = np.random.randint(0, len(repeat_policies))
          add_repeat_ids.append(repeat_ids[index])
      else:
        raise ValueError("Unrecognized br_selection method: %s"
                         % br_selection)

    for add_repeat_id in add_repeat_ids:
      per_player_repeats[player][add_repeat_id] += 1

    for add_novel_policy in add_novel_policies:
      per_player_policies[player].append(add_novel_policy)  # Add new policy.
      per_player_repeats[player].append(1)  # Add new count.
      per_player_num_novel_policies[player] += 1

  # Add new joint policies.
  for pids in itertools.product(*[
      range(len(policies)) for policies in per_player_policies]):
    if pids in joint_policies:
      continue
    logging.debug("Evaluating novel joint policy: %s.", pids)
    policies = [
        policies[pid] for pid, policies in zip(pids, per_player_policies)]
    policies = tuple(map(policy.python_policy_to_pyspiel_policy, policies))
    pyspiel_tabular_policy = pyspiel.to_joint_tabular_policy(policies, True)
    joint_policies[pids] = pyspiel_tabular_policy
    joint_returns[pids] = [
        0.0 if abs(er) < RETURN_TOL else er
        for er in pyspiel.expected_returns(
            game.new_initial_state(), pyspiel_tabular_policy, -1, True)]

  return per_player_num_novel_policies

