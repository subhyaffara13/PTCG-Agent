
def evolve_mean_field_game(mfg_game,
                           policy,
                           graph,
                           scaling=1,
                           frequency_printing=1):
  distribution_mfg = distribution_module.DistributionPolicy(mfg_game, policy)
  root_state = mfg_game.new_initial_state()
  listing_states = [root_state]

  # plot_network_mean_field_game(graph, {origin: 1})
  i = 0
  while not listing_states[0].is_terminal() and not all(
      state._vehicle_without_legal_action for state in listing_states):  # pylint:disable=protected-access
    assert abs(sum(map(distribution_mfg.value, listing_states)) - 1) < 1e-4, (
        f"{list(map(distribution_mfg.value, listing_states))}")
    new_listing_states = []
    list_of_state_seen = set()
    # In case chance node:
    if listing_states[0].current_player() == pyspiel.PlayerId.CHANCE:
      for mfg_state in listing_states:
        for action, _ in mfg_state.chance_outcomes():
          new_mfg_state = mfg_state.child(action)
          # Do not append twice the same file.
          if str(new_mfg_state) not in list_of_state_seen:
            new_listing_states.append(new_mfg_state)
          list_of_state_seen.add(str(new_mfg_state))
      current_distribution = {}
      for mfg_state in new_listing_states:
        location = mfg_state._vehicle_location  # pylint:disable=protected-access
        if location not in current_distribution:
          current_distribution[location] = 0
        current_distribution[location] += distribution_mfg.value(mfg_state)
      plot_network_mean_field_game(graph, current_distribution, scaling=scaling)

    # In case mean field node:
    elif listing_states[0].current_player() == pyspiel.PlayerId.MEAN_FIELD:
      for mfg_state in listing_states:
        dist_to_register = mfg_state.distribution_support()

        def get_probability_for_state(str_state):
          try:
            return distribution_mfg.value_str(str_state)
          except ValueError:
            return 0

        dist = [
            get_probability_for_state(str_state)
            for str_state in dist_to_register
        ]
        new_mfg_state = mfg_state.clone()
        new_mfg_state.update_distribution(dist)
        # Do not append twice the same file.
        if str(new_mfg_state) not in list_of_state_seen:
          new_listing_states.append(new_mfg_state)
        list_of_state_seen.add(str(new_mfg_state))

    # In case action node:
    else:
      assert (listing_states[0].current_player() ==
              pyspiel.PlayerId.DEFAULT_PLAYER_ID), "The player id should be 0"
      for mfg_state in listing_states:
        for action, _ in policy.action_probabilities(mfg_state).items():
          new_mfg_state = mfg_state.child(action)
          # Do not append twice the same file.
          if str(new_mfg_state) not in list_of_state_seen:
            new_listing_states.append(new_mfg_state)
          list_of_state_seen.add(str(new_mfg_state))
      current_distribution = {}
      for mfg_state in new_listing_states:
        location = mfg_state._vehicle_location  # pylint:disable=protected-access
        if location not in current_distribution:
          current_distribution[location] = 0
        current_distribution[location] += distribution_mfg.value(mfg_state)
      assert abs(sum(current_distribution.values()) - 1) < 1e-4, (
          f"{current_distribution}")
      i += 1
      if i % frequency_printing == 0:
        plot_network_mean_field_game(
            graph, current_distribution, scaling=scaling)
    listing_states = new_listing_states

