
def get_current_and_average_payoffs(ps2ro_trainer, current_player,
                                    current_strategy):
  """Returns the current player's and average players' payoffs.

  These payoffs are returned when current_player's strategy's index is
  'current_strategy'.

  Args:
    ps2ro_trainer: A ps2ro object.
    current_player: Integer, current player index.
    current_strategy: Integer, current player's strategy index.

  Returns:
    Payoff tensor for current player, Average payoff tensor over all players.
  """
  # Get the vector of payoffs associated with current_player's strategy ind
  meta_games = ps2ro_trainer.meta_games
  current_payoff = meta_games[current_player]
  current_payoff = np.take(
      current_payoff, current_strategy, axis=current_player)

  # Get average per-player payoff matrix.
  average_payoffs = np.mean(meta_games, axis=0)
  average_payoffs = np.take(
      average_payoffs, current_strategy, axis=current_player)
  return current_payoff, average_payoffs

