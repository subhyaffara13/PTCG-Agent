
def make_single_env(game_name, seed):

  def gen_env():
    game = pyspiel.load_game(game_name)
    return Environment(game, chance_event_sampler=ChanceEventSampler(seed=seed))

  return gen_env

