import re

def _playthrough_params(lines):
  """Returns the playthrough parameters from a playthrough record.

  Args:
    lines: The playthrough as a list of lines.

  Returns:
    A `dict` with entries:
      game_string: string, e.g. 'markov_soccer'.
      action_sequence: a list of action choices made in the playthrough.
    Suitable for passing to playthrough to re-generate the playthrough.

  Raises:
    ValueError if the playthrough is not valid.
  """
  params = {"action_sequence": []}
  use_action_ids = _USE_ACTION_IDS.value
  for line in lines:
    match_game = re.fullmatch(r"game: (.*)", line)
    match_observation_params = re.fullmatch(r"observation_params: (.*)", line)
    match_update_distribution = (line == "action: update_distribution")
    if use_action_ids:
      match_action = re.fullmatch(r"action: (.*)", line)
      match_actions = re.fullmatch(r"actions: \[(.*)\]", line)
    else:
      match_action = re.fullmatch(r'# Apply action "(.*)"', line)
      match_actions = re.fullmatch(r"# Apply joint action \[(.*)\]", line)
    if match_game:
      params["game_string"] = match_game.group(1)
    elif match_observation_params:
      params["observation_params_string"] = match_observation_params.group(1)
    elif match_update_distribution:
      params["action_sequence"].append("update_distribution")
    elif match_action:
      matched = match_action.group(1)
      if use_action_ids:
        params["action_sequence"].append(int(matched))
      else:
        params["action_sequence"].append(matched)
    elif match_actions:
      if use_action_ids:
        params["action_sequence"].append(
            [int(x) for x in match_actions.group(1).split(", ")])
      else:
        params["action_sequence"].append(
            [x[1:-1] for x in match_actions.group(1).split(", ")])
  if "game_string" in params:
    return params
  raise ValueError("Could not find params")

