import logging

def print_iteration(actions, state):
  """Print actions and state."""
  logging.info("Action taken by agent 0: %s", Action(actions[0]).name)
  logging.info("Action taken by agent 1: %s", Action(actions[1]).name)
  logging.info("Board state:\n %s", state)
  logging.info("-" * 80)


def print_iteration(time_step, actions, player_id):
  """Print TimeStep information."""
  obs = time_step.observations
  logging.info("Player: %s", player_id)
  if time_step.step_type.first():
    logging.info("Info state: %s, - - %s", obs["info_state"][player_id],
                 time_step.step_type)
  else:
    logging.info("Info state: %s, %s %s %s", obs["info_state"][player_id],
                 time_step.rewards[player_id], time_step.discounts[player_id],
                 time_step.step_type)
  logging.info("Action taken: %s", actions)
  logging.info("-" * 80)


def print_iteration(time_step, player_id, action=None):
  """Print TimeStep information."""
  obs = time_step.observations
  logging.info("Player: %s", player_id)
  if time_step.first():
    logging.info("Info state: %s, - - %s", obs["info_state"][player_id],
                 time_step.step_type)
  else:
    logging.info("Info state: %s, %s %s %s", obs["info_state"][player_id],
                 time_step.rewards[player_id], time_step.discounts[player_id],
                 time_step.step_type)
  if action is not None:
    logging.info("Action taken: %s", action)
  logging.info("-" * 80)

