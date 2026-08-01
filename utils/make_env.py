
def make_env(raw_env):
    def env(**kwargs):
        env = raw_env(**kwargs)
        if env.continuous_actions:
            env = wrappers.ClipOutOfBoundsWrapper(env)
        else:
            env = wrappers.AssertOutOfBoundsWrapper(env)
        env = wrappers.OrderEnforcingWrapper(env)
        return env

    return env


def make_env(game: str, iterations: int, batch_size: int) -> Environment:
  """Creates an environment.

  The environment is either iterated prisoners dilemma or iterated matching
  pennies.
  
  Args:
      game: The game to play. Either 'ipd' or 'imp'.
      iterations: The number of iterations to play.
      batch_size: The batch size.

  Returns:
      An environment instance.
  """
  if game == 'ipd':
    env = IteratedPrisonersDilemma(iterations=iterations, batch_size=batch_size)
  elif game == 'imp':
    env = IteratedMatchingPennies(iterations=iterations, batch_size=batch_size)
  else:
    raise ValueError(f'Unknown game: {game}')
  return env

