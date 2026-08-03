from typing import Optional

def playthrough_lines(game_string, alsologtostdout=False, action_sequence=None,
                      observation_params_string=None,
                      seed: Optional[int] = None):
  """Returns a playthrough of the specified game as a list of lines.

  Actions are selected uniformly at random, including chance actions.

  Args:
    game_string: string, e.g. 'markov_soccer' or 'kuhn_poker(players=4)'.
    alsologtostdout: Whether to also print the trace to stdout. This can be
      useful when an error occurs, to still be able to get context information.
    action_sequence: A (possibly partial) list of action choices to make.
    observation_params_string: Optional observation parameters for constructing
      an observer.
    seed: A(n optional) seed to initialize the random number generator from.
  """
  should_display_state_fn = ShouldDisplayStateTracker()
  lines = []
  action_sequence = action_sequence or []
  should_display = True

  def add_line(v, force=False):
    if force or should_display:
      if alsologtostdout:
        print(v)
      lines.append(v)

  game = pyspiel.load_game(game_string)
  add_line("game: {}".format(game_string))
  if observation_params_string:
    add_line("observation_params: {}".format(observation_params_string))
  if seed is None:
    seed = np.random.randint(2**32 - 1)
  game_type = game.get_type()

  observation_params = (
      pyspiel.game_parameters_from_string(observation_params_string)
      if observation_params_string
      else None
  )
  default_observation = make_observation(
      game,
      imperfect_information_observation_type=None,
      params=observation_params,
  )

  infostate_observation = make_observation(
      game, pyspiel.IIGObservationType(perfect_recall=True)
  )

  public_observation = None
  private_observation = None

  # Instantiate factored observations only for imperfect information games,
  # as it would yield unncessarily redundant information for perfect info games.
  # The default observation is the same as the public observation, while private
  # observations are always empty.
  if game_type.information == game_type.Information.IMPERFECT_INFORMATION:
    public_observation = make_observation(
        game,
        pyspiel.IIGObservationType(
            public_info=True,
            perfect_recall=False,
            private_info=pyspiel.PrivateInfoType.NONE,
        ),
    )
    private_observation = make_observation(
        game,
        pyspiel.IIGObservationType(
            public_info=False,
            perfect_recall=False,
            private_info=pyspiel.PrivateInfoType.SINGLE_PLAYER,
        ),
    )

  add_line("")
  add_line("GameType.chance_mode = {}".format(game_type.chance_mode))
  add_line("GameType.dynamics = {}".format(game_type.dynamics))
  add_line("GameType.information = {}".format(game_type.information))
  add_line("GameType.long_name = {}".format('"{}"'.format(game_type.long_name)))
  add_line("GameType.max_num_players = {}".format(game_type.max_num_players))
  add_line("GameType.min_num_players = {}".format(game_type.min_num_players))
  add_line("GameType.parameter_specification = {}".format("[{}]".format(
      ", ".join('"{}"'.format(param)
                for param in sorted(game_type.parameter_specification)))))
  add_line("GameType.provides_information_state_string = {}".format(
      game_type.provides_information_state_string))
  add_line("GameType.provides_information_state_tensor = {}".format(
      game_type.provides_information_state_tensor))
  add_line("GameType.provides_observation_string = {}".format(
      game_type.provides_observation_string))
  add_line("GameType.provides_observation_tensor = {}".format(
      game_type.provides_observation_tensor))
  add_line("GameType.provides_factored_observation_string = {}".format(
      game_type.provides_factored_observation_string))
  add_line("GameType.reward_model = {}".format(game_type.reward_model))
  add_line("GameType.short_name = {}".format('"{}"'.format(
      game_type.short_name)))
  add_line("GameType.utility = {}".format(game_type.utility))

  add_line("")
  add_line("NumDistinctActions() = {}".format(game.num_distinct_actions()))
  add_line("PolicyTensorShape() = {}".format(game.policy_tensor_shape()))
  add_line("MaxChanceOutcomes() = {}".format(game.max_chance_outcomes()))
  add_line("GetParameters() = {}".format(_format_params(game.get_parameters())))
  add_line("NumPlayers() = {}".format(game.num_players()))
  add_line("MinUtility() = {:.5}".format(game.min_utility()))
  add_line("MaxUtility() = {:.5}".format(game.max_utility()))
  add_line("UtilitySum() = {}".format(game.utility_sum()))
  if infostate_observation and infostate_observation.tensor is not None:
    add_line("InformationStateTensorShape() = {}".format(
        format_shapes(infostate_observation.dict)))
    add_line("InformationStateTensorLayout() = {}".format(
        game.information_state_tensor_layout()))
    add_line("InformationStateTensorSize() = {}".format(
        len(infostate_observation.tensor)))
  if default_observation and default_observation.tensor is not None:
    add_line("ObservationTensorShape() = {}".format(
        format_shapes(default_observation.dict)))
    add_line("ObservationTensorLayout() = {}".format(
        game.observation_tensor_layout()))
    add_line("ObservationTensorSize() = {}".format(
        len(default_observation.tensor)))
  add_line("MaxGameLength() = {}".format(game.max_game_length()))
  add_line('ToString() = "{}"'.format(str(game)))

  players = list(range(game.num_players()))
  # Arbitrarily pick the last possible initial states (for all games
  # but multi-population MFGs, there will be a single initial state).
  state = game.new_initial_states()[-1]
  state_idx = 0
  rng = np.random.RandomState(seed)

  while True:
    should_display = should_display_state_fn(state)
    add_line("", force=True)
    add_line("# State {}".format(state_idx), force=True)
    for line in str(state).splitlines():
      add_line("# {}".format(line).rstrip())
    add_line("IsTerminal() = {}".format(state.is_terminal()))
    add_line("History() = {}".format([int(a) for a in state.history()]))
    add_line('HistoryString() = "{}"'.format(state.history_str()))
    add_line("IsChanceNode() = {}".format(state.is_chance_node()))
    add_line("IsSimultaneousNode() = {}".format(state.is_simultaneous_node()))
    add_line("CurrentPlayer() = {}".format(state.current_player()))
    if infostate_observation:
      for player in players:
        s = infostate_observation.string_from(state, player)
        if s is not None:
          add_line(f'InformationStateString({player}) = "{_escape(s)}"')
    if infostate_observation and infostate_observation.tensor is not None:
      for player in players:
        infostate_observation.set_from(state, player)
        for name, tensor in infostate_observation.dict.items():
          label = f"InformationStateTensor({player})"
          label += f".{name}" if name != "info_state" else ""
          for line in _format_tensor(tensor, label):
            add_line(line)
    if default_observation:
      for player in players:
        s = default_observation.string_from(state, player)
        if s is not None:
          add_line(f'ObservationString({player}) = "{_escape(s)}"')
    if public_observation:
      s = public_observation.string_from(state, 0)
      if s is not None:
        add_line('PublicObservationString() = "{}"'.format(_escape(s)))
      for player in players:
        s = private_observation.string_from(state, player)
        if s is not None:
          add_line(f'PrivateObservationString({player}) = "{_escape(s)}"')
    if default_observation and default_observation.tensor is not None:
      for player in players:
        default_observation.set_from(state, player)
        for name, tensor in default_observation.dict.items():
          label = f"ObservationTensor({player})"
          label += f".{name}" if name != "observation" else ""
          for line in _format_tensor(tensor, label):
            add_line(line)
    if game_type.chance_mode == pyspiel.GameType.ChanceMode.SAMPLED_STOCHASTIC:
      add_line('SerializeState() = "{}"'.format(_escape(state.serialize())))
    if not state.is_chance_node():
      add_line("Rewards() = {}".format(_format_float_vector(state.rewards())))
      add_line("Returns() = {}".format(_format_float_vector(state.returns())))
    if state.is_terminal():
      break
    if state.is_chance_node():
      add_line("ChanceOutcomes() = {}".format(
          _format_chance_outcomes(state.chance_outcomes())))
    if state.is_mean_field_node():
      add_line("DistributionSupport() = {}".format(
          state.distribution_support()))
      num_states = len(state.distribution_support())
      state.update_distribution(
          [1. / num_states] * num_states if num_states else [])
      if state_idx < len(action_sequence):
        assert action_sequence[state_idx] == "update_distribution", (
            f"Unexpected action at MFG node: {action_sequence[state_idx]}, "
            f"state: {state}, action_sequence: {action_sequence}")
      add_line("")
      add_line("# Set mean field distribution to be uniform", force=True)
      add_line("action: update_distribution", force=True)
    elif state.is_simultaneous_node():
      for player in players:
        add_line("LegalActions({}) = [{}]".format(
            player, ", ".join(str(x) for x in state.legal_actions(player))))
      for player in players:
        add_line("StringLegalActions({}) = [{}]".format(
            player, ", ".join('"{}"'.format(state.action_to_string(player, x))
                              for x in state.legal_actions(player))))
      if state_idx < len(action_sequence):
        actions = action_sequence[state_idx]
        for i, a in enumerate(actions):
          if isinstance(a, str):
            actions[i] = state.string_to_action(i, a)
      else:
        actions = []
        for pl in players:
          legal_actions = state.legal_actions(pl)
          actions.append(0 if not legal_actions else rng.choice(legal_actions))
      add_line("")
      add_line("# Apply joint action [{}]".format(
          format(", ".join(
              '"{}"'.format(state.action_to_string(player, action))
              for player, action in enumerate(actions)))), force=True)
      add_line("actions: [{}]".format(", ".join(
          str(action) for action in actions)), force=True)
      state.apply_actions(actions)
    else:
      add_line("LegalActions() = [{}]".format(", ".join(
          str(x) for x in state.legal_actions())))
      add_line("StringLegalActions() = [{}]".format(", ".join(
          '"{}"'.format(state.action_to_string(state.current_player(), x))
          for x in state.legal_actions())))
      if state_idx < len(action_sequence):
        action = action_sequence[state_idx]
        if isinstance(action, str):
          action = state.string_to_action(state.current_player(), action)
      else:
        action = rng.choice(state.legal_actions())
      add_line("")
      add_line('# Apply action "{}"'.format(
          state.action_to_string(state.current_player(), action)), force=True)
      add_line("action: {}".format(action), force=True)
      state.apply_action(action)
    state_idx += 1
  return lines

