
def _play_against_random(game, agent, n):
  reward = 0
  for _ in range(n):
    reward += _play_once_against_random(game, agent)
  return reward / n

