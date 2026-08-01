
def test_policy_on_game(self, game, policy_object, player=-1):
  """Checks the policy conforms to the conventions.

  Checks the Policy.action_probabilities contains only legal actions (but not
  necessarily all).
  Checks that the probabilities are positive and sum to 1.

  Args:
    self: The Test class. This methid targets as being used as a utility
      function to test policies.
    game: A `pyspiel.Game`, same as the one used in the policy.
    policy_object: A `policy.Policy` object on `game`. to test.
    player: Restrict testing policy to a player.
  """

  all_states = get_all_states.get_all_states(
      game,
      depth_limit=-1,
      include_terminals=False,
      include_chance_states=False,
      to_string=lambda s: s.information_state_string())

  for state in all_states.values():
    legal_actions = set(state.legal_actions())
    action_probabilities = policy_object.action_probabilities(state)

    for action in action_probabilities.keys():
      # We want a clearer error message to be able to debug.
      actions_missing = set(legal_actions) - set(action_probabilities.keys())
      illegal_actions = set(action_probabilities.keys()) - set(legal_actions)
      self.assertIn(
          action,
          legal_actions,
          msg="The action {} is present in the policy but is not a legal "
          "actions (these are {})\n"
          "Legal actions missing from policy: {}\n"
          "Illegal actions present in policy: {}".format(
              action, legal_actions, actions_missing, illegal_actions))

    sum_ = 0
    for prob in action_probabilities.values():
      sum_ += prob
      self.assertGreaterEqual(prob, 0)
    if player < 0 or state.current_player() == player:
      self.assertAlmostEqual(1, sum_)
    else:
      self.assertAlmostEqual(0, sum_)

