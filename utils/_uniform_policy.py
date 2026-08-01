
def _uniform_policy(state):
  legal_actions = state.legal_actions()
  return [(action, 1.0 / len(legal_actions)) for action in legal_actions]


def _uniform_policy(size):
  if size > 0:
    return [1./size]*size
  return []

