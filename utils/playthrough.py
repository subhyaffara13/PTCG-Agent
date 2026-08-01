
def playthrough(game_string,
                action_sequence,
                alsologtostdout=False,
                observation_params_string=None,
                seed: Optional[int] = None):
  """Returns a playthrough of the specified game as a single text.

  Actions are selected uniformly at random, including chance actions.

  Args:
    game_string: string, e.g. 'markov_soccer', with possible optional params,
      e.g. 'go(komi=4.5,board_size=19)'.
    action_sequence: A (possibly partial) list of action choices to make.
    alsologtostdout: Whether to also print the trace to stdout. This can be
      useful when an error occurs, to still be able to get context information.
    observation_params_string: Optional observation parameters for constructing
      an observer.
    seed: A(n optional) seed to initialize the random number generator from.
  """
  lines = playthrough_lines(game_string, alsologtostdout, action_sequence,
                            observation_params_string, seed)
  return "\n".join(lines) + "\n"

