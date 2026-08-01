
def load_bot(bot_type: str, pid: int) -> pyspiel.Bot:
  if bot_type == "human":
    return human.HumanBot()
  elif bot_type == "uniform":
    return uniform_random.UniformRandomBot(pid, np.random)

