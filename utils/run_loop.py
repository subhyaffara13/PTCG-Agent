import logging

def run_loop(game,
             game_name,
             seed=0,
             iterations=40,
             policy_init="uniform",
             update_players_strategy="all",
             target_equilibrium="cce",
             br_selection="largest_gap",
             train_meta_solver="mgcce",
             eval_meta_solver="mwcce",
             ignore_repeats=False,
             initialize_callback=None,
             action_value_tolerance=-1.0,
             callback=None):
  """Runs JPSRO."""
  if initialize_callback is None:
    initialize_callback = initialize_callback_
  if callback is None:
    callback = callback_
  kwargs = dict(
      game=game,
      game_name=game_name,
      seed=seed,
      iterations=iterations,
      policy_init=policy_init,
      update_players_strategy=update_players_strategy,
      target_equilibrium=target_equilibrium,
      br_selection=br_selection,
      train_meta_solver=train_meta_solver,
      eval_meta_solver=eval_meta_solver,
      ignore_repeats=ignore_repeats,
  )

  # Set seed.
  np.random.seed(seed)

  # Some statistics.
  num_players = game.num_players()  # Look in the game.

  # Initialize.
  values = initialize(game, train_meta_solver, eval_meta_solver, policy_init,
                      ignore_repeats, br_selection)

  # Initialize Callback.
  (iteration,
   per_player_repeats,
   per_player_policies,
   joint_policies,
   joint_returns,
   meta_games,
   train_meta_dists,
   eval_meta_dists,
   train_meta_values,
   eval_meta_values,
   train_meta_gaps,
   eval_meta_gaps,
   checkpoint) = initialize_callback(*values, game)

  # Run JPSRO.
  while iteration <= iterations:
    logging.debug("Beginning JPSRO iteration %03d", iteration)
    per_player_new_policies, per_player_gaps_train = find_best_response(
        game,
        train_meta_dists[-1],
        meta_games[-1],
        iteration,
        joint_policies,
        target_equilibrium,
        update_players_strategy,
        action_value_tolerance,
    )
    train_meta_gaps.append([sum(gaps) for gaps in per_player_gaps_train])
    _, per_player_gaps_eval = find_best_response(
        game,
        eval_meta_dists[-1],
        meta_games[-1],
        iteration,
        joint_policies,
        target_equilibrium,
        update_players_strategy,
        action_value_tolerance,
    )
    eval_meta_gaps.append([sum(gaps) for gaps in per_player_gaps_eval])
    per_player_num_novel_policies = add_new_policies(
        per_player_new_policies, per_player_gaps_train, per_player_repeats,
        per_player_policies, joint_policies, joint_returns, game, br_selection)
    del per_player_num_novel_policies
    add_meta_game(
        meta_games,
        per_player_policies,
        joint_returns)
    add_meta_dist(
        train_meta_dists, train_meta_values, train_meta_solver,
        meta_games[-1], per_player_repeats, ignore_repeats)
    add_meta_dist(
        eval_meta_dists, eval_meta_values, eval_meta_solver,
        meta_games[-1], per_player_repeats, ignore_repeats)

    # Stats.
    per_player_num_policies = train_meta_dists[-1].shape[:]
    log_string = LOG_STRING.format(
        iteration=iteration,
        game=game_name,
        player=("{: 12d}" * num_players).format(*list(range(num_players))),
        brs="",
        num_policies=("{: 12d}" * num_players).format(*[
            sum(ppr) for ppr in per_player_repeats]),
        unique=("{: 12d}" * num_players).format(*per_player_num_policies),
        train_meta_solver=train_meta_solver,
        train_value=("{: 12g}" * num_players).format(*train_meta_values[-1]),
        train_gap=("{: 12g}" * num_players).format(*train_meta_gaps[-1]),
        eval_meta_solver=eval_meta_solver,
        eval_value=("{: 12g}" * num_players).format(*eval_meta_values[-1]),
        eval_gap=("{: 12g}" * num_players).format(*eval_meta_gaps[-1]),
    )
    logging.info(log_string)

    # Increment.
    iteration += 1

    # Callback.
    checkpoint = callback(
        iteration,
        per_player_repeats,
        per_player_policies,
        joint_policies,
        joint_returns,
        meta_games,
        train_meta_dists,
        eval_meta_dists,
        train_meta_values,
        eval_meta_values,
        train_meta_gaps,
        eval_meta_gaps,
        kwargs,
        checkpoint)

