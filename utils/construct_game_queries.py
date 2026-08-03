import itertools

def construct_game_queries(base_profile, num_checkpts):
  """Constructs a list of checkpoint selection tuples to query value function.

  Each query tuple (key, query) where key = (pi, pj) and query is
  (p1's selected checkpt, ..., p7's selected checkpt) fixes the players in the
  game of diplomacy to be played. It may be necessary to play several games with
  the same players to form an accurate estimate of the value or payoff for each
  player as checkpts contain stochastic policies.

  Args:
    base_profile: list of selected checkpts for each player, i.e.,
      a sample from the player strategy profile ([x_i ~ p(x_i)])
    num_checkpts: list of ints, number of strats (or ckpts) per player
  Returns:
    Set of query tuples containing a selected checkpoint index for each player.
  """
  new_queries = set([])

  num_players = len(base_profile)
  for pi, pj in itertools.combinations(range(num_players), 2):
    new_profile = list(base_profile)
    for ai in range(num_checkpts[pi]):
      new_profile[pi] = ai
      for aj in range(num_checkpts[pj]):
        new_profile[pj] = aj
        query = tuple(new_profile)
        pair = (pi, pj)
        new_queries.update([(pair, query)])

  return new_queries


def construct_game_queries(base_profile, num_checkpts):
  """Constructs a list of checkpoint selection tuples to query value function.

  Each query tuple (p1's selected checkpt, ..., p7's selected checkpt)
  fixes the players in the game of diplomacy to be played. It may be necessary
  to play several games with the same players to form an accurate estimate of
  the value or payoff for each player as checkpts contain stochastic policies.

  Args:
    base_profile: list of selected checkpts for each player, i.e.,
      a sample from the player strategy profile ([x_i ~ p(x_i)])
    num_checkpts: number of checkpts available to each player
  Returns:
    Set of query tuples containing a selected checkpoint index for each player.
  """
  new_queries = set([])

  pi, pj = 0, 1
  new_profile = list(base_profile)
  for ai in range(num_checkpts):
    new_profile[pi] = ai
    for aj in range(num_checkpts):
      new_profile[pj] = aj
      query = tuple(new_profile)
      new_queries.update([query])

  return new_queries

