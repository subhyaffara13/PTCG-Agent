
def rectified_selector(ps2ro_trainer, current_player, current_strategy):
  current_payoff, average_payoffs = get_current_and_average_payoffs(
      ps2ro_trainer, current_player, current_strategy)

  # Rectified Nash condition : select those strategies where we do better
  # than others.
  res = current_payoff >= average_payoffs
  return np.expand_dims(res, axis=current_player)

