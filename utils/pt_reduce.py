
def pt_reduce(payoff_tensor, strats, remove_players):
  """Computes possible payoffs for remove_players with others' strats fixed.

  This is equivalent to the Jacobian of the payoff w.r.t. remove_players:
  sum_{a...z} A_k * x_1a * ... * x_nz for player k.
  Args:
    payoff_tensor: a single player k's payoff tensor, i.e.,
      a num action x ... x num action (num player) np.array
    strats: list of distributions over strategies for each player
    remove_players: players to NOT sum over in expectation
  Returns:
    payoff tensor of shape: num_action x ... x num_action,
      num_action for each player in remove_players
  """
  result = np.copy(payoff_tensor)
  result_dims = list(range(len(result.shape)))
  other_player_idxs = list(result_dims)
  for remove_player in remove_players:
    other_player_idxs.remove(remove_player)
  for other_player_idx in other_player_idxs:
    new_result_dims = list(result_dims)
    new_result_dims.remove(other_player_idx)
    result = np.einsum(result, result_dims, strats[other_player_idx],
                       [other_player_idx], new_result_dims)
    result_dims = new_result_dims
  return result

