
def iterated_dominance(game_or_payoffs, mode, tol=1e-7):
  """Reduces a strategy space using iterated dominance.

  See: http://www.smallparty.com/yoram/classes/principles/nash.pdf

  Args:
    game_or_payoffs: either a pyspiel matrix- or normal-form game, or a payoff
      tensor of dimension `num_players` + 1. First dimension is the player,
      followed by the actions of all players, e.g. a 3x3 game (2 players) has
      dimension [2,3,3].
    mode: DOMINANCE_STRICT, DOMINANCE_WEAK, or DOMINANCE_VERY_WEAK
    tol: tolerance

  Returns:
    A tuple (`reduced_game`, `live_actions`).
    * if `game_or_payoffs` is an instance of `pyspiel.MatrixGame`, so is
      `reduced_game`; otherwise `reduced_game` is a payoff tensor.
    * `live_actions` is a tuple of length `num_players`, where
      `live_actions[player]` is a boolean vector of shape `num_actions`;
       `live_actions[player][action]` is `True` if `action` wasn't dominated for
       `player`.
  """
  payoffs = (
      utils.game_payoffs_array(game_or_payoffs)
      if isinstance(game_or_payoffs, pyspiel.NormalFormGame)
      else np.asarray(game_or_payoffs, dtype=np.float64)
  )
  live_actions = [
      np.ones(num_actions, bool) for num_actions in payoffs.shape[1:]
  ]
  progress = True
  while progress:
    progress = False
    # trying faster method first
    for method in ("pure", "mixed"):
      if progress:
        continue
      for player, live in enumerate(live_actions):
        if live.sum() == 1:
          # one action is dominant
          continue

        # discarding all dominated opponent actions
        payoffs_live = payoffs[player]
        for opponent in range(payoffs.shape[0]):
          if opponent != player:
            payoffs_live = payoffs_live.compress(
                live_actions[opponent], opponent
            )

        # reshaping to (player_actions, joint_opponent_actions)
        payoffs_live = np.moveaxis(payoffs_live, player, 0)
        payoffs_live = payoffs_live.reshape((payoffs_live.shape[0], -1))

        for action in range(live.size):
          if not live[action]:
            continue
          if method == "pure":
            # mark all actions that `action` dominates
            advantage = payoffs_live[action] - payoffs_live
            dominated = _pure_dominated_from_advantages(advantage, mode, tol)
            dominated[action] = False
            dominated &= live
            if dominated.any():
              progress = True
              live &= ~dominated
              if live.sum() == 1:
                break
          if method == "mixed":
            # test if `action` is dominated by a mixed policy
            mixture = is_dominated(
                live[:action].sum(),
                payoffs_live[live],
                0,
                mode,
                tol,
                return_mixture=True,
            )
            if mixture is None:
              continue
            # if it is, mark any other actions dominated by that policy
            progress = True
            advantage = mixture.dot(payoffs_live[live]) - payoffs_live[live]
            dominated = _pure_dominated_from_advantages(advantage, mode, tol)
            dominated[mixture > tol] = False
            assert dominated[live[:action].sum()]
            live.put(live.nonzero()[0], ~dominated)
            if live.sum() == 1:
              break

  for player, live in enumerate(live_actions):
    payoffs = payoffs.compress(live, player + 1)

  if isinstance(game_or_payoffs, pyspiel.MatrixGame):
    return (
        pyspiel.MatrixGame(
            game_or_payoffs.get_type(),
            game_or_payoffs.get_parameters(),
            [
                game_or_payoffs.row_action_name(action)
                for action in live_actions[0].nonzero()[0]
            ],
            [
                game_or_payoffs.col_action_name(action)
                for action in live_actions[1].nonzero()[0]
            ],
            *payoffs,
        ),
        live_actions,
    )
  else:
    return payoffs, live_actions

