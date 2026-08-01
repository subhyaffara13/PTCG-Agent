
def _assert_is_perfect_recall(game):
  """Raises an AssertionError if the game is not perfect recall.

  We are willing to ensure the following property (perfect recall):
  - define X_i(h) be the sequence of information states and actions from the
    start of the game observed by player i (i.e. excluding the states and
    actions taken by the opponents unless those actions are included in player
    i's information state), along h but not including the state at h:
       X_i(h) = (s_1, a_1), (s_2, a_2), ... , (s_{t-1}, a_{t-1})
    then player i has perfect recall in this game iff: forall s in S_i,
    forall h1, h2 in s X_i(h1) == X_i(h2). Here, we check that the game has
    perfect recall if this is true for all players i (excluding chance).

    For more detail and context, see page 11 of
    http://mlanctot.info/files/papers/PhD_Thesis_MarcLanctot.pdf

  In particular, note that:
  - we want to check that holds both for
    + `std::string information_state_string(current_player)`
    + `information_state_tensor`.
  - we check that currently only from the point of view of the current
    player at the information state (i.e. we compare
    `prev_state.information_state_string(current_player)` but not
    `prev_state.information_state_string(opponent_player)`

  The strategy is the following: we traverse the full tree (of states, not
  infostates), and make sure for each node that the history we get for
  the infostate associated to that node, that is is unique with respect to
  the infostate.

  Args:
    game: A Spiel game to check.

  Returns:
    The internal cache mapping (infostate_str, player_id) to a list of one
    history leading to this infostate.
  """
  game_info = game.get_type()
  if game_info.dynamics != pyspiel.GameType.Dynamics.SEQUENTIAL:
    raise ValueError("The game is expected to be sequential")

  infostate_player_to_history = {}
  _assert_is_perfect_recall_recursive(
      game.new_initial_state(),
      current_history=[],
      infostate_player_to_history=infostate_player_to_history)

  return infostate_player_to_history

