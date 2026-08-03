import random

def _select_random_legal_action(time_step):
  cur_legal_actions = time_step.observations["legal_actions"][0]
  action = random.choice(cur_legal_actions)
  return action


def _select_random_legal_action(time_step):
  cur_legal_actions = time_step.observations["legal_actions"][0]
  action = random.choice(cur_legal_actions)
  return action

