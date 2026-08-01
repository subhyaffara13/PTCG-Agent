
def sample_bot_agent(pid, bot_names, population_ids, num_actions):
  idx = np.random.randint(0, len(population_ids))
  bot_id = population_ids[idx]
  name = bot_names[bot_id]
  bot = pyspiel.make_roshambo_bot(pid, name)
  return BotAgent(num_actions, bot, name=name), bot_id

