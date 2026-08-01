
def make_single_atari_env(gym_id,
                          seed,
                          idx,
                          capture_video,
                          run_name,
                          use_episodic_life_env=True):
  """Make the single-agent Atari environment."""

  def gen_env():
    game = pyspiel.load_game(
        "atari", {
            "gym_id": gym_id,
            "seed": seed,
            "idx": idx,
            "capture_video": capture_video,
            "run_name": run_name,
            "use_episodic_life_env": use_episodic_life_env
        })
    return Environment(
        game,
        chance_event_sampler=ChanceEventSampler(seed=seed),
        observation_type=ObservationType.OBSERVATION)

  return gen_env

