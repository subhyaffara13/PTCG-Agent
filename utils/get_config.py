
def get_config():
    """Create, populate and return the VersioneerConfig() object."""
    # these strings are filled in when 'setup.py versioneer' creates
    # _version.py
    cfg = VersioneerConfig()
    cfg.VCS = "git"
    cfg.style = "pep440"
    cfg.tag_prefix = "v"
    cfg.parentdir_prefix = "pandas-"
    cfg.versionfile_source = "pandas/_version.py"
    cfg.verbose = False
    return cfg


def get_config(
    args: Iterable[str] | None = None,
    plugins: Sequence[str | _PluggyPlugin] | None = None,
    *,
    prog: str | None = None,
) -> Config:
    # Subsequent calls to main will create a fresh instance.
    pluginmanager = PytestPluginManager()
    invocation_params = Config.InvocationParams(
        args=args or (),
        plugins=plugins,
        dir=pathlib.Path.cwd(),
    )
    config = Config(pluginmanager, invocation_params=invocation_params, prog=prog)

    if invocation_params.args:
        # Handle any "-p no:plugin" args.
        pluginmanager.consider_preparse(invocation_params.args, exclude_only=True)

    for spec in default_plugins:
        pluginmanager.import_plugin(spec)

    return config


def get_config() -> Config:
    """Get the config object for the global Application instance, if there is one

    otherwise return an empty config object
    """
    if Application.initialized():
        return Application.instance().config
    else:
        return Config()


def get_config(config: Union[ConfigDict, Type[object], None]) -> Type[BaseConfig]:
    if config is None:
        return BaseConfig

    else:
        config_dict = (
            config
            if isinstance(config, dict)
            else {k: getattr(config, k) for k in dir(config) if not k.startswith('__')}
        )

        class Config(BaseConfig):
            ...

        for k, v in config_dict.items():
            setattr(Config, k, v)
        return Config


def get_config():
  """Get configuration for imitation dataset construction."""
  config = ml_collections.config_dict.ConfigDict()

  config.game_string = "chat_game"
  config.game_id = 0
  config.seed = 34239871
  config.num_demos = 10
  config.num_iters = 4
  config.domain = Domain.SCHEDULE_MEETING_W_TONE

  if config.domain == Domain.DEBATE_W_STYLE:
    config = get_config_debate(config)
  elif config.domain == Domain.TRADE_FRUIT_W_TONE:
    config = get_config_trade_fruit_w_tone(config)
  elif config.domain == Domain.SCHEDULE_MEETING_W_DOW:
    config = get_config_schedule_meeting_w_dow(config)
    config.substrate = schedules
  elif config.domain == Domain.SCHEDULE_MEETING_W_TONE:
    config = get_config_schedule_meeting_w_tone(config)
  else:
    raise ValueError("Unknown domain: %s" % config.domain)

  return config


def get_config():
  """Get configuration for imitation dataset construction."""
  config = ml_collections.config_dict.ConfigDict()

  config.game_string = "chat_game"
  config.seed = 34239871
  config.num_iters = 4
  config.num_trials = 10
  config.num_candidates = 2
  config.domain = Domain.SCHEDULE_MEETING_W_TONE

  if config.domain == Domain.TRADE_FRUIT_W_TONE:
    config.env_config = config_trade_fruit_w_tone.get_config()
  elif config.domain == Domain.SCHEDULE_MEETING_W_TONE:
    config.env_config = config_schedule_meeting_w_tone.get_config()
  else:
    raise ValueError("Unknown domain: %s" % config.domain)

  return config


def get_config():
  """Get configuration for chat game."""
  config = config_dict.ConfigDict()

  num_players = 2

  observations = [
      obs_utils.Observation(summary_debate.PREFIX, summary_debate.POSTFIX)
      for _ in range(num_players)
  ]

  header = env_debate_with_style_info.HEADER

  payoffs = [payoffs_debate.PAYOFF]

  examples_names = names_debate.NAMES

  given_prompt_actions = collections.OrderedDict()
  given_prompt_actions[header.action_keys[0]] = arguments.STYLES + ['any']
  num_styles = len(arguments.STYLES) + 1

  given_private_info = collections.OrderedDict()
  given_private_info['info'] = ['Argue for the topic statement.',
                                'Argue against the topic statement.']
  given_private_info['topic'] = [scenario_debate.TOPIC_B,
                                 scenario_debate.TOPIC_B]

  scenario_a = env_debate_with_style_info.Scenario(
      '',
      'Bob',
      'Alice',
      'logos',
      scenario_debate.TOPIC_B,
      'Argue for the topic statement.')

  examples_scenarios = [scenario_a]

  llm_termination_prompt = scenario_debate.LLM_TERMINATION_PROMPT

  params = {'num_distinct_actions': num_players * num_styles,
            'num_llm_seeds': 2,
            'num_init_states': 3,
            'num_players': num_players,
            'min_utility': min([float(p.min) for p in payoffs]),
            'max_utility': max([float(p.max) for p in payoffs]),
            'num_max_replies': 1,
            'silence_logging': True}

  config.params = params

  config.game = config_dict.ConfigDict()
  config.game.observations = observations
  config.game.header = header
  config.game.payoffs = payoffs
  config.game.given_prompt_actions = given_prompt_actions
  config.game.num_names = 10
  config.game.num_private_info = (2, 2)
  config.game.examples_names = examples_names
  config.game.given_private_info = given_private_info
  config.game.examples_scenarios = examples_scenarios
  config.game.llm_list_suffix = 'Output: '
  config.game.llm_termination_prompt = llm_termination_prompt

  return config


def get_config():
  """Get configuration for chat game."""
  config = config_dict.ConfigDict()

  num_players = 2

  observations = [
      obs_utils.Observation(summary_debate.PREFIX, summary_debate.POSTFIX)
      for _ in range(num_players)
  ]

  header = env_debate_with_style_info.HEADER

  payoffs = [payoffs_debate.PAYOFF]

  given_prompt_actions = collections.OrderedDict()
  given_prompt_actions[header.action_keys[0]] = arguments.STYLES + ['any']
  num_styles = len(arguments.STYLES) + 1

  given_private_info = collections.OrderedDict()
  given_private_info['info'] = ['Argue for the topic statement.',
                                'Argue against the topic statement.']
  given_private_info['topic'] = [scenario_debate.TOPIC_B,
                                 scenario_debate.TOPIC_B]

  initial_scenario = env_debate_with_style_info.Scenario(
      '',
      'Bob',
      'Alice',
      'logos',
      scenario_debate.TOPIC_B,
      'Argue for the topic statement.')

  llm_termination_prompt = scenario_debate.LLM_TERMINATION_PROMPT

  params = {'num_distinct_actions': num_players * num_styles,
            'num_llm_seeds': 2,
            'num_init_states': 1,
            'num_players': num_players,
            'min_utility': min([float(p.min) for p in payoffs]),
            'max_utility': max([float(p.max) for p in payoffs]),
            'num_max_replies': 1}

  config.params = params

  config.game = config_dict.ConfigDict()
  config.game.observations = observations
  config.game.header = header
  config.game.payoffs = payoffs
  config.game.given_prompt_actions = given_prompt_actions
  config.game.num_private_info = (2, 2)
  config.game.given_names = ['Bob', 'Alice']
  config.game.given_private_info = given_private_info
  config.game.initial_scenario = initial_scenario
  config.game.llm_list_suffix = 'Output: '
  config.game.llm_termination_prompt = llm_termination_prompt

  return config


def get_config():
  """Get configuration for chat game."""
  config = config_dict.ConfigDict()

  observations = [obs_utils.Observation(),
                  obs_utils.Observation()]

  header = email_with_tone.HEADER

  payoffs = [sentiment.PAYOFF,
             sentiment.PAYOFF]

  given_names = ['Bob',
                 'Suzy']
  num_players = len(given_names)

  given_llm_seeds = [12345]

  given_prompt_actions = collections.OrderedDict()
  tones = ['Happy',
           'Sad',
           'Angry',
           'Calm']
  given_prompt_actions[header.action_keys[0]] = tones
  num_tones = len(tones)

  # Vacuous message
  message = '\n\n'.join(text_utils.wrap(
      ['Hi {receiver},', 'I hope you are well,', 'Best,', '{sender}']
      ))
  initial_scenario = email_with_tone.Scenario(message, 'Bob', 'Suzy', 'Calm')

  query = ('Read the following message. Does it appear that ' +
           'the relevant parties have agreed on a deal? ' +
           'After reading the message, respond Yes or No. ' +
           'Here is the message:\n\n{msg}\n\n')
  llm_termination_prompt = term_utils.Termination(query, '', '')

  params = {'num_distinct_actions': num_players * num_tones,
            'num_llm_seeds': 1,
            'num_init_states': 1,
            'num_players': num_players,
            'min_utility': min([float(p.min) for p in payoffs]),
            'max_utility': max([float(p.max) for p in payoffs]),
            'num_max_replies': 2}

  config.params = params

  config.game = config_dict.ConfigDict()
  config.game.observations = observations
  config.game.header = header
  config.game.payoffs = payoffs
  config.game.given_names = given_names
  config.game.given_llm_seeds = given_llm_seeds
  config.game.given_prompt_actions = given_prompt_actions
  config.game.initial_scenario = initial_scenario
  config.game.llm_list_suffix = 'Output: '
  config.game.llm_termination_prompt = llm_termination_prompt

  return config


def get_config():
  """Get configuration for chat game."""
  config = config_dict.ConfigDict()

  num_players = 3

  observations = [
      obs_utils.Observation(summary.PREFIX, summary.POSTFIX)
      for _ in range(num_players)
  ]

  scenario_a = email_with_tone.Scenario(rwn.SCENARIO_A, 'Alice', 'Bob')
  scenario_b = email_with_tone.Scenario(rwn.SCENARIO_B, 'Joel', 'Gene')
  scenario_c = email_with_tone.Scenario(rwn.SCENARIO_C, 'George', 'Jill')
  examples_scenarios = [scenario_a,
                        scenario_b,
                        scenario_c]

  header = email_with_tone.HEADER

  payoffs = [sentiment.PAYOFF]

  examples_names = names.NAMES

  examples_prompt_actions = collections.OrderedDict()
  examples_prompt_actions[header.action_keys[0]] = tones.TONES
  num_tones = 3

  query = ('Read the following message. Does it appear that ' +
           'the relevant parties have agreed on a deal? ' +
           'After reading the message, respond Yes or No. ' +
           'Here is the message:\n\n{msg}\n\n')
  llm_termination_prompt = term_utils.Termination(query, '', '')

  params = {'num_distinct_actions': num_players * num_tones,
            'num_llm_seeds': 2,
            'num_init_states': 3,
            'num_players': num_players,
            'min_utility': min([float(p.min) for p in payoffs]),
            'max_utility': max([float(p.max) for p in payoffs]),
            'num_max_replies': 2}

  config.params = params

  config.game = config_dict.ConfigDict()
  config.game.observations = observations
  config.game.header = header
  config.game.payoffs = payoffs
  config.game.num_names = 10
  config.game.num_prompt_actions = (num_tones,)
  config.game.num_private_info = (3,)
  config.game.examples_names = examples_names
  config.game.examples_prompt_actions = examples_prompt_actions
  config.game.examples_scenarios = examples_scenarios
  config.game.llm_list_suffix = 'Output: '
  config.game.llm_termination_prompt = llm_termination_prompt

  return config


def get_config():
  """Get configuration for chat game."""
  config = config_dict.ConfigDict()

  num_players = 3

  observations = [
      obs_utils.Observation(summary.PREFIX, summary.POSTFIX)
      for _ in range(num_players)
  ]

  scenario_a = email_with_tone.Scenario(rwn.SCENARIO_A, 'Alice', 'Bob')
  scenario_b = email_with_tone.Scenario(rwn.SCENARIO_B, 'Joel', 'Gene')
  scenario_c = email_with_tone.Scenario(rwn.SCENARIO_C, 'George', 'Jill')
  examples_scenarios = [scenario_a,
                        scenario_b,
                        scenario_c]

  header = email_with_tone.HEADER

  payoffs = [sentiment.PAYOFF]

  examples_names = names.NAMES

  examples_prompt_actions = collections.OrderedDict()
  examples_prompt_actions[header.action_keys[0]] = tones.TONES
  num_tones = 3

  query = ('Read the following message. Does it appear that ' +
           'the relevant parties have agreed on a deal? ' +
           'After reading the message, respond Yes or No. ' +
           'Here is the message:\n\n{msg}\n\n')
  llm_termination_prompt = term_utils.Termination(query, '', '')

  params = {'num_distinct_actions': num_players * num_tones,
            'num_llm_seeds': 2,
            'num_init_states': 3,
            'num_players': num_players,
            'min_utility': min([float(p.min) for p in payoffs]),
            'max_utility': max([float(p.max) for p in payoffs]),
            'num_max_replies': 2}

  config.params = params

  config.game = config_dict.ConfigDict()
  config.game.observations = observations
  config.game.header = header
  config.game.payoffs = payoffs
  config.game.num_names = 10
  config.game.num_prompt_actions = (num_tones,)
  config.game.num_private_info = (3,)
  config.game.examples_names = examples_names
  config.game.examples_prompt_actions = examples_prompt_actions
  config.game.examples_scenarios = examples_scenarios
  config.game.llm_list_suffix = 'Output: '
  config.game.llm_termination_prompt = llm_termination_prompt

  return config


def get_config():
  """Get configuration for chat game."""
  config = config_dict.ConfigDict()

  num_players = 2

  observations = [
      obs_utils.Observation(summary.PREFIX, summary.POSTFIX)
      for _ in range(num_players)
  ]

  header = env_schedule_meeting_with_info.HEADER

  payoffs = [payoffs_schedule_meeting.PAYOFF]

  examples_names = names_schedule_meeting.NAMES

  examples_private_info = collections.OrderedDict()
  examples_private_info['ooo_days'] = [scenario_schedule_meeting.OOO_A,
                                       scenario_schedule_meeting.OOO_B]
  examples_private_info['day_prefs'] = [scenario_schedule_meeting.DAY_PREFS_A,
                                        scenario_schedule_meeting.DAY_PREFS_B]

  scenario_a = env_schedule_meeting_with_info.Scenario(
      scenario_schedule_meeting.SCENARIO_A,
      'Bob',
      'Suzy',
      scenario_schedule_meeting.OOO_A,
      scenario_schedule_meeting.DAY_PREFS_A)
  scenario_b = env_schedule_meeting_with_info.Scenario(
      scenario_schedule_meeting.SCENARIO_B,
      'Jill',
      'George',
      scenario_schedule_meeting.OOO_B,
      scenario_schedule_meeting.DAY_PREFS_B)

  examples_scenarios = [scenario_a, scenario_b]

  llm_termination_prompt = scenario_schedule_meeting.LLM_TERMINATION_PROMPT

  params = {'num_distinct_actions': num_players,
            'num_llm_seeds': 2,
            'num_init_states': 3,
            'num_players': num_players,
            'min_utility': min([float(p.min) for p in payoffs]),
            'max_utility': max([float(p.max) for p in payoffs]),
            'num_max_replies': 3}

  config.params = params

  config.game = config_dict.ConfigDict()
  config.game.observations = observations
  config.game.header = header
  config.game.payoffs = payoffs
  config.game.num_names = 10
  config.game.num_private_info = (3, 3)
  config.game.examples_names = examples_names
  config.game.examples_private_info = examples_private_info
  config.game.examples_scenarios = examples_scenarios
  config.game.llm_list_suffix = 'Output: '
  config.game.llm_termination_prompt = llm_termination_prompt

  return config


def get_config():
  """Get configuration for chat game."""
  config = config_dict.ConfigDict()

  num_players = 2

  observations = [
      obs_utils.Observation(summary.PREFIX, summary.POSTFIX)
      for _ in range(num_players)
  ]

  header = env_schedule_meeting_with_dow_info.HEADER

  payoffs = [payoffs_schedule_meeting.PAYOFF]

  examples_names = names_schedule_meeting.NAMES

  given_prompt_actions = collections.OrderedDict()
  days = ['Monday',
          'Tuesday',
          'Wednesday',
          'Thursday',
          'Friday',
          'Saturday',
          'Sunday']
  given_prompt_actions[header.action_keys[0]] = days + ['any']
  num_days = len(days) + 1

  examples_private_info = collections.OrderedDict()
  examples_private_info['ooo_days'] = [scenario_schedule_meeting.OOO_A,
                                       scenario_schedule_meeting.OOO_B]
  examples_private_info['day_prefs'] = [scenario_schedule_meeting.DAY_PREFS_A,
                                        scenario_schedule_meeting.DAY_PREFS_B]

  scenario_a = env_schedule_meeting_with_dow_info.Scenario(
      scenario_schedule_meeting.SCENARIO_A,
      'Bob',
      'Suzy',
      scenario_schedule_meeting.OOO_A,
      scenario_schedule_meeting.DAY_PREFS_A,
      'Thursday')
  scenario_b = env_schedule_meeting_with_dow_info.Scenario(
      scenario_schedule_meeting.SCENARIO_B,
      'Jill',
      'George',
      scenario_schedule_meeting.OOO_B,
      scenario_schedule_meeting.DAY_PREFS_B,
      'Friday')

  examples_scenarios = [scenario_a, scenario_b]

  llm_termination_prompt = scenario_schedule_meeting.LLM_TERMINATION_PROMPT

  params = {'num_distinct_actions': num_players * num_days,
            'num_llm_seeds': 2,
            'num_init_states': 3,
            'num_players': num_players,
            'min_utility': min([float(p.min) for p in payoffs]),
            'max_utility': max([float(p.max) for p in payoffs]),
            'num_max_replies': 1,
            'silence_logging': True}

  config.params = params

  config.game = config_dict.ConfigDict()
  config.game.observations = observations
  config.game.header = header
  config.game.payoffs = payoffs
  config.game.given_prompt_actions = given_prompt_actions
  config.game.num_names = 10
  config.game.num_prompt_actions = (num_days,)
  config.game.num_private_info = (3, 3)
  config.game.examples_names = examples_names
  config.game.examples_private_info = examples_private_info
  config.game.examples_scenarios = examples_scenarios
  config.game.llm_list_suffix = 'Output: '
  config.game.llm_termination_prompt = llm_termination_prompt

  return config


def get_config():
  """Get configuration for chat game."""
  config = config_dict.ConfigDict()

  num_players = 2

  observations = [
      obs_utils.Observation(summary.PREFIX, summary.POSTFIX)
      for _ in range(num_players)
  ]

  header = env_schedule_meeting_with_dow_info.HEADER

  payoffs = [payoffs_schedule_meeting.PAYOFF]

  given_prompt_actions = collections.OrderedDict()
  days = ['Monday',
          'Tuesday',
          'Wednesday',
          'Thursday',
          'Friday',
          'Saturday',
          'Sunday']
  given_prompt_actions[header.action_keys[0]] = days + ['any']
  num_days = len(days) + 1

  given_private_info = collections.OrderedDict()
  given_private_info['day_prefs'] = [scenario_schedule_meeting.DAY_PREFS_A,
                                     scenario_schedule_meeting.DAY_PREFS_B]
  given_private_info['ooo_days'] = [scenario_schedule_meeting.OOO_A,
                                    scenario_schedule_meeting.OOO_B]

  scenario_a = env_schedule_meeting_with_dow_info.Scenario(
      scenario_schedule_meeting.SCENARIO_A,
      'Bob',
      'Suzy',
      scenario_schedule_meeting.OOO_A,
      scenario_schedule_meeting.DAY_PREFS_A,
      'Thursday')

  llm_termination_prompt = scenario_schedule_meeting.LLM_TERMINATION_PROMPT

  params = {'num_distinct_actions': num_players * num_days,
            'num_llm_seeds': 2,
            'num_init_states': 1,
            'num_players': num_players,
            'min_utility': min([float(p.min) for p in payoffs]),
            'max_utility': max([float(p.max) for p in payoffs]),
            'num_max_replies': 1,
            'silence_logging': True}

  config.params = params

  config.game = config_dict.ConfigDict()
  config.game.observations = observations
  config.game.header = header
  config.game.payoffs = payoffs
  config.game.given_prompt_actions = given_prompt_actions
  config.game.num_private_info = (2, 2)
  config.game.given_names = ['Bob', 'Suzy']
  config.game.given_private_info = given_private_info
  config.game.initial_scenario = scenario_a
  config.game.llm_list_suffix = 'Output: '
  config.game.llm_termination_prompt = llm_termination_prompt

  return config


def get_config():
  """Get configuration for chat game."""
  config = config_dict.ConfigDict()

  num_players = 2

  observations = [
      obs_utils.Observation(summary.PREFIX, summary.POSTFIX)
      for _ in range(num_players)
  ]

  header = env_schedule_meeting_with_tone_info.HEADER

  payoffs = [payoffs_schedule_meeting.PAYOFF]

  examples_names = names_schedule_meeting.NAMES

  given_prompt_actions = collections.OrderedDict()
  tones = ['calm',
           'assertive',
           'submissive',
           'any']
  given_prompt_actions[header.action_keys[0]] = tones
  num_tones = len(tones)

  examples_private_info = collections.OrderedDict()
  examples_private_info['ooo_days'] = [scenario_schedule_meeting.OOO_A,
                                       scenario_schedule_meeting.OOO_B]
  examples_private_info['day_prefs'] = [scenario_schedule_meeting.DAY_PREFS_A,
                                        scenario_schedule_meeting.DAY_PREFS_B]

  scenario_a = env_schedule_meeting_with_tone_info.Scenario(
      scenario_schedule_meeting.SCENARIO_A,
      'Bob',
      'Suzy',
      scenario_schedule_meeting.OOO_A,
      scenario_schedule_meeting.DAY_PREFS_A,
      'calm')
  scenario_b = env_schedule_meeting_with_tone_info.Scenario(
      scenario_schedule_meeting.SCENARIO_B,
      'Jill',
      'George',
      scenario_schedule_meeting.OOO_B,
      scenario_schedule_meeting.DAY_PREFS_B,
      'assertive')

  examples_scenarios = [scenario_a, scenario_b]

  llm_termination_prompt = scenario_schedule_meeting.LLM_TERMINATION_PROMPT

  params = {'num_distinct_actions': num_players * num_tones,
            'num_llm_seeds': 1,
            'num_init_states': 3,
            'num_players': num_players,
            'min_utility': min([float(p.min) for p in payoffs]),
            'max_utility': max([float(p.max) for p in payoffs]),
            'num_max_replies': 1,
            'silence_logging': True}

  config.params = params

  config.game = config_dict.ConfigDict()
  config.game.observations = observations
  config.game.header = header
  config.game.payoffs = payoffs
  config.game.given_prompt_actions = given_prompt_actions
  config.game.num_names = 10
  config.game.num_prompt_actions = (num_tones,)
  config.game.num_private_info = (3, 3)
  config.game.examples_names = examples_names
  config.game.examples_private_info = examples_private_info
  config.game.examples_scenarios = examples_scenarios
  config.game.llm_list_suffix = 'Output: '
  config.game.llm_termination_prompt = llm_termination_prompt

  return config


def get_config():
  """Get configuration for chat game."""
  config = config_dict.ConfigDict()

  num_players = 2

  observations = [
      obs_utils.Observation(summary.PREFIX, summary.POSTFIX)
      for _ in range(num_players)
  ]

  header = env_schedule_meeting_with_tone_info.HEADER

  payoffs = [payoffs_schedule_meeting.PAYOFF]

  given_prompt_actions = collections.OrderedDict()
  tones = ['calm',
           'assertive',
           'submissive',
           'any']
  given_prompt_actions[header.action_keys[0]] = tones
  num_tones = len(tones)

  given_private_info = collections.OrderedDict()
  given_private_info['day_prefs'] = [scenario_schedule_meeting.DAY_PREFS_A,
                                     scenario_schedule_meeting.DAY_PREFS_B]
  given_private_info['ooo_days'] = [scenario_schedule_meeting.OOO_A,
                                    scenario_schedule_meeting.OOO_B]

  scenario_a = env_schedule_meeting_with_tone_info.Scenario(
      scenario_schedule_meeting.SCENARIO_A,
      'Bob',
      'Suzy',
      scenario_schedule_meeting.OOO_A,
      scenario_schedule_meeting.DAY_PREFS_A,
      'calm')

  llm_termination_prompt = scenario_schedule_meeting.LLM_TERMINATION_PROMPT

  params = {'num_distinct_actions': num_players * num_tones,
            'num_llm_seeds': 2,
            'num_init_states': 1,
            'num_players': num_players,
            'min_utility': min([float(p.min) for p in payoffs]),
            'max_utility': max([float(p.max) for p in payoffs]),
            'num_max_replies': 1,
            'silence_logging': True}

  config.params = params

  config.game = config_dict.ConfigDict()
  config.game.observations = observations
  config.game.header = header
  config.game.payoffs = payoffs
  config.game.given_prompt_actions = given_prompt_actions
  config.game.num_private_info = (2, 2)
  config.game.given_names = ['Bob', 'Suzy']
  config.game.given_private_info = given_private_info
  config.game.initial_scenario = scenario_a
  config.game.llm_list_suffix = 'Output: '
  config.game.llm_termination_prompt = llm_termination_prompt

  return config


def get_config():
  """Get configuration for chat game."""
  config = config_dict.ConfigDict()

  num_players = 2

  observations = [
      obs_utils.Observation(summary.PREFIX, summary.POSTFIX)
      for _ in range(num_players)
  ]

  header = env_trade_fruit_with_info.HEADER

  payoffs = [payoffs_trade_fruit.PAYOFF]

  examples_names = names_trade_fruit.NAMES

  examples_private_info = collections.OrderedDict()
  examples_private_info['fruit_endowment'] = [scenario_trade_fruit.ENDOWMENT_A,
                                              scenario_trade_fruit.ENDOWMENT_B]
  examples_private_info['fruit_valuations'] = [scenario_trade_fruit.VALUATION_A,
                                               scenario_trade_fruit.VALUATION_B]

  scenario_a = env_trade_fruit_with_info.Scenario(
      scenario_trade_fruit.SCENARIO_A,
      'Bob',
      'Suzy',
      scenario_trade_fruit.ENDOWMENT_A,
      scenario_trade_fruit.VALUATION_A)
  scenario_b = env_trade_fruit_with_info.Scenario(
      scenario_trade_fruit.SCENARIO_B,
      'Jill',
      'George',
      scenario_trade_fruit.ENDOWMENT_B,
      scenario_trade_fruit.VALUATION_B)
  examples_scenarios = [scenario_a, scenario_b]

  llm_termination_prompt = scenario_trade_fruit.LLM_TERMINATION_PROMPT

  params = {'num_distinct_actions': num_players,
            'num_llm_seeds': 2,
            'num_init_states': 3,
            'num_players': num_players,
            'min_utility': min([float(p.min) for p in payoffs]),
            'max_utility': max([float(p.max) for p in payoffs]),
            'num_max_replies': 3}

  config.params = params

  config.game = config_dict.ConfigDict()
  config.game.observations = observations
  config.game.header = header
  config.game.payoffs = payoffs
  config.game.num_names = 10
  config.game.num_private_info = (3, 3)
  config.game.examples_names = examples_names
  config.game.examples_private_info = examples_private_info
  config.game.examples_scenarios = examples_scenarios
  config.game.llm_list_suffix = 'Output: '
  config.game.llm_termination_prompt = llm_termination_prompt

  return config


def get_config():
  """Get configuration for chat game."""
  config = config_dict.ConfigDict()

  num_players = 2

  observations = [
      obs_utils.Observation(summary.PREFIX, summary.POSTFIX)
      for _ in range(num_players)
  ]

  header = env_trade_fruit_with_tone_info.HEADER

  payoffs = [payoffs_trade_fruit.PAYOFF]

  examples_names = names_trade_fruit.NAMES

  given_prompt_actions = collections.OrderedDict()
  tones = ['calm',
           'assertive',
           'submissive',
           'any']
  given_prompt_actions[header.action_keys[0]] = tones
  num_tones = len(tones)

  examples_private_info = collections.OrderedDict()
  examples_private_info['fruit_endowment'] = [scenario_trade_fruit.ENDOWMENT_A,
                                              scenario_trade_fruit.ENDOWMENT_B]
  examples_private_info['fruit_valuations'] = [scenario_trade_fruit.VALUATION_A,
                                               scenario_trade_fruit.VALUATION_B]

  scenario_a = env_trade_fruit_with_tone_info.Scenario(
      scenario_trade_fruit.SCENARIO_A,
      'Bob',
      'Suzy',
      scenario_trade_fruit.ENDOWMENT_A,
      scenario_trade_fruit.VALUATION_A,
      'calm')
  scenario_b = env_trade_fruit_with_tone_info.Scenario(
      scenario_trade_fruit.SCENARIO_B,
      'Jill',
      'George',
      scenario_trade_fruit.ENDOWMENT_B,
      scenario_trade_fruit.VALUATION_B,
      'calm')

  examples_scenarios = [scenario_a, scenario_b]

  llm_termination_prompt = scenario_trade_fruit.LLM_TERMINATION_PROMPT

  params = {'num_distinct_actions': num_players * num_tones,
            'num_llm_seeds': 2,
            'num_init_states': 3,
            'num_players': num_players,
            'min_utility': min([float(p.min) for p in payoffs]),
            'max_utility': max([float(p.max) for p in payoffs]),
            'num_max_replies': 1,
            'silence_logging': True}

  config.params = params

  config.game = config_dict.ConfigDict()
  config.game.observations = observations
  config.game.header = header
  config.game.payoffs = payoffs
  config.game.given_prompt_actions = given_prompt_actions
  config.game.num_names = 10
  config.game.num_prompt_actions = (num_tones,)
  config.game.num_private_info = (3, 3)
  config.game.examples_names = examples_names
  config.game.examples_private_info = examples_private_info
  config.game.examples_scenarios = examples_scenarios
  config.game.llm_list_suffix = 'Output: '
  config.game.llm_termination_prompt = llm_termination_prompt

  return config


def get_config():
  """Get configuration for chat game."""
  config = config_dict.ConfigDict()

  num_players = 2

  observations = [
      obs_utils.Observation(summary.PREFIX, summary.POSTFIX)
      for _ in range(num_players)
  ]

  header = env_trade_fruit_with_tone_info.HEADER

  payoffs = [payoffs_trade_fruit.PAYOFF]

  given_prompt_actions = collections.OrderedDict()
  tones = ['calm',
           'assertive',
           'submissive',
           'any']
  given_prompt_actions[header.action_keys[0]] = tones
  num_tones = len(tones)

  given_private_info = collections.OrderedDict()
  given_private_info['fruit_endowment'] = [scenario_trade_fruit.ENDOWMENT_A,
                                           scenario_trade_fruit.ENDOWMENT_B]
  given_private_info['fruit_valuations'] = [scenario_trade_fruit.VALUATION_A,
                                            scenario_trade_fruit.VALUATION_B]

  scenario_a = env_trade_fruit_with_tone_info.Scenario(
      scenario_trade_fruit.SCENARIO_A,
      'Bob',
      'Suzy',
      scenario_trade_fruit.ENDOWMENT_A,
      scenario_trade_fruit.VALUATION_A,
      'calm')

  llm_termination_prompt = scenario_trade_fruit.LLM_TERMINATION_PROMPT

  params = {'num_distinct_actions': num_players * num_tones,
            'num_llm_seeds': 2,
            'num_init_states': 1,
            'num_players': num_players,
            'min_utility': min([float(p.min) for p in payoffs]),
            'max_utility': max([float(p.max) for p in payoffs]),
            'num_max_replies': 1,
            'silence_logging': True}

  config.params = params

  config.game = config_dict.ConfigDict()
  config.game.observations = observations
  config.game.header = header
  config.game.payoffs = payoffs
  config.game.given_prompt_actions = given_prompt_actions
  config.game.num_private_info = (2, 2)
  config.game.given_names = ['Bob', 'Suzy']
  config.game.given_private_info = given_private_info
  config.game.initial_scenario = scenario_a
  config.game.llm_list_suffix = 'Output: '
  config.game.llm_termination_prompt = llm_termination_prompt

  return config


def get_config():
  config = config_dict.ConfigDict()
  config.field1 = 1
  config.field2 = 'tom'
  config.nested = config_dict.ConfigDict()
  config.nested.field = 2.23
  config.tuple = (1, 2, 3)
  return config


def get_config(config_string):
  """Return an instance of ConfigDict depending on `config_string`."""
  possible_structures = {
      'linear':
          config_dict.ConfigDict({
              'model_constructor': 'snt.Linear',
              'model_config': config_dict.ConfigDict({
                  'output_size': 42,
              })
          }),
      'lstm':
          config_dict.ConfigDict({
              'model_constructor': 'snt.LSTM',
              'model_config': config_dict.ConfigDict({
                  'hidden_size': 108,
              })
          })
  }

  return possible_structures[config_string]


def get_config():
  """Returns a ConfigDict. Used for tests."""
  cfg = config_dict.ConfigDict()
  cfg.integer = 1
  cfg.reference = config_dict.FieldReference(1)
  cfg.list = [1, 2, 3]
  cfg.nested_list = [[1, 2, 3]]
  cfg.nested_configdict = config_dict.ConfigDict()
  cfg.nested_configdict.integer = 1
  cfg.unusable_config = UnusableConfig()

  return cfg


def get_config():
  cfg = config_dict.ConfigDict()
  cfg.ref = config_dict.FieldReference(123)
  cfg.ref_nodefault = config_dict.placeholder(int)
  return cfg


def get_config():
  cfg = config_dict.ConfigDict()
  cfg.integer = config_dict.placeholder(object)
  cfg.string = config_dict.placeholder(object)
  cfg.nested = config_dict.placeholder(object)
  cfg.other_with_default = config_dict.placeholder(object)
  cfg.other_with_default = 123
  cfg.other_with_default_overitten = config_dict.placeholder(object)
  cfg.other_with_default_overitten = 123
  return cfg


def get_config():
  cfg = MiniConfig()
  cfg['entry_with_collision'] = False
  cfg.entry_with_collision = True
  return cfg


def get_config():

  config = TestConfig()
  config.object = TestConfig()
  config.object_reference = config.object
  config.object_copy = copy.deepcopy(config.object)

  return config


def get_config(config_string):
  """A config which takes an extra string argument."""
  possible_configs = {
      'type_a': config_dict.ConfigDict({
          'thing_a': 23,
          'thing_b': 42,
      }),
      'type_b': config_dict.ConfigDict({
          'thing_a': 19,
          'thing_c': 65,
      }),
  }
  return possible_configs[config_string]


def get_config():
  return {'item': type_error_function()}


def get_config():
  return {'item': value_error_function()}


def get_config():
  """Returns a ConfigDict instance describing a complex config.

  Returns:
    A ConfigDict instance with the structure:

    ```
        CONFIG-+-- integer
               |-- float
               |-- string
               |-- bool
               |-- dict +-- integer
               |        |-- float
               |        |-- string
               |        |-- bool
               |        |-- dict +-- float
               |
               |-- object +-- integer
               |          |-- float
               |          |-- string
               |          |-- bool
               |          |-- dict +-- integer
               |                   |-- float
               |                   |-- string
               |                   |-- bool
               |                   |-- dict +-- float
               |
               |-- object_copy +-- integer
               |               |-- float
               |               |-- string
               |               |-- bool
               |               |-- dict +-- integer
               |                        |-- float
               |                        |-- string
               |                        |-- bool
               |                        |-- dict +-- float
               |
               |-- object_reference [reference pointing to CONFIG-+--object]
    ```
  """
  config = _get_flat_config()
  config.object = _get_flat_config()

  # References work just fine, so you will be able to override both
  # values at the same time. The rule is the same as for python objects,
  # everything that is mutable is passed as a reference, thus it will not work
  # with assigning integers or strings, but will work just fine with
  # ConfigDicts.
  # WARNING: Each time you assign a dictionary as a value it will create a new
  # instance of ConfigDict in memory, thus it will be a copy of the original
  # dict and not a reference to the original.
  config.object_reference = config.object

  # ConfigDict supports deepcopying.
  config.object_copy = copy.deepcopy(config.object)

  return config

