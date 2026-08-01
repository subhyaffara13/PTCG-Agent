
def find_best_response(
    game,
    meta_dist,
    meta_game,
    iteration,
    joint_policies,
    target_equilibrium,
    update_players_strategy,
    action_value_tolerance,
):
  """Returns new best response policies."""
  num_players = meta_game.shape[0]
  per_player_num_policies = meta_dist.shape[:]

  # Player update strategy.
  if update_players_strategy == "all":
    players = list(range(num_players))
  elif update_players_strategy == "cycle":
    players = [iteration % num_players]
  elif update_players_strategy == "random":
    players = [np.random.randint(0, num_players)]
  else:
    raise ValueError(
        "update_players_strategy must be a valid player update strategy: "
        "%s. Received: %s" % (UPDATE_PLAYERS_STRATEGY, update_players_strategy))

  # Find best response.
  per_player_new_policies = []
  per_player_deviation_incentives = []

  if target_equilibrium == "cce":
    for player in range(num_players):
      if player in players:
        joint_policy_ids = itertools.product(*[
            (np_-1,) if p_ == player else range(np_) for p_, np_
            in enumerate(per_player_num_policies)])
        joint_policies_slice = [
            joint_policies[jpid] for jpid in joint_policy_ids]
        meta_dist_slice = np.sum(meta_dist, axis=player)
        meta_dist_slice[meta_dist_slice < DIST_TOL] = 0.0
        meta_dist_slice[meta_dist_slice > 1.0] = 1.0
        meta_dist_slice /= np.sum(meta_dist_slice)
        meta_dist_slice = meta_dist_slice.flat

        mu = [(p, mp) for mp, p in zip(joint_policies_slice, meta_dist_slice)
              if p > 0]
        info = pyspiel.cce_dist(
            game,
            mu,
            player,
            prob_cut_threshold=0.0,
            action_value_tolerance=action_value_tolerance)

        new_policy = policy.pyspiel_policy_to_python_policy(
            game, info.best_response_policies[0], players=(player,))
        on_policy_value = np.sum(meta_game[player] * meta_dist)
        deviation_incentive = max(
            info.best_response_values[0] - on_policy_value, 0)
        if deviation_incentive < GAP_TOL:
          deviation_incentive = 0.0

        per_player_new_policies.append([new_policy])
        per_player_deviation_incentives.append([deviation_incentive])
      else:
        per_player_new_policies.append([])
        per_player_deviation_incentives.append([])

  elif target_equilibrium == "ce":
    for player in range(num_players):
      if player in players:
        per_player_new_policies.append([])
        per_player_deviation_incentives.append([])

        for pid in range(per_player_num_policies[player]):
          joint_policy_ids = itertools.product(*[
              (pid,) if p_ == player else range(np_) for p_, np_
              in enumerate(per_player_num_policies)])
          joint_policies_slice = [
              joint_policies[jpid] for jpid in joint_policy_ids]
          inds = tuple((pid,) if player == p_ else slice(None)
                       for p_ in range(num_players))
          meta_dist_slice = np.ravel(meta_dist[inds]).copy()
          meta_dist_slice[meta_dist_slice < DIST_TOL] = 0.0
          meta_dist_slice[meta_dist_slice > 1.0] = 1.0
          meta_dist_slice_sum = np.sum(meta_dist_slice)

          if meta_dist_slice_sum > 0.0:
            meta_dist_slice /= meta_dist_slice_sum
            mu = [(p, mp) for mp, p in
                  zip(joint_policies_slice, meta_dist_slice)
                  if p > 0]
            info = pyspiel.cce_dist(
                game,
                mu,
                player,
                prob_cut_threshold=0.0,
                action_value_tolerance=action_value_tolerance)

            new_policy = policy.pyspiel_policy_to_python_policy(
                game, info.best_response_policies[0], players=(player,))
            on_policy_value = np.sum(
                np.ravel(meta_game[player][inds]) * meta_dist_slice)
            deviation_incentive = max(
                info.best_response_values[0] - on_policy_value, 0)
            if deviation_incentive < GAP_TOL:
              deviation_incentive = 0.0

            per_player_new_policies[-1].append(new_policy)
            per_player_deviation_incentives[-1].append(
                meta_dist_slice_sum * deviation_incentive)

      else:
        per_player_new_policies.append([])
        per_player_deviation_incentives.append([])

  else:
    raise ValueError(
        "target_equilibrium must be a valid best response strategy: %s. "
        "Received: %s" % (BRS, target_equilibrium))

  return per_player_new_policies, per_player_deviation_incentives

