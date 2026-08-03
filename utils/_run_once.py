import time

def _run_once(state, bots):
  """Plays bots with each other, returns terminal utility for each player."""
  for bot in bots:
    bot.restart_at(state)
  while not state.is_terminal():
    if state.is_chance_node():
      outcomes, probs = zip(*state.chance_outcomes())
      state.apply_action(np.random.choice(outcomes, p=probs))
    else:
      state.apply_action(bots[state.current_player()].step(state)[1])
  return state


def _run_once(state, bots, net, params):
  """Plays bots with each other, returns terminal utility for each player."""
  for bot in bots:
    bot.restart()
  while not state.is_terminal():
    if state.is_chance_node():
      outcomes, probs = zip(*state.chance_outcomes())
      state.apply_action(np.random.choice(outcomes, p=probs))
    else:
      if FLAGS.sleep:
        time.sleep(FLAGS.sleep)  # wait for the human to see how it goes
      if state.current_player() % 2 == 1:
        # Have simplest play for now
        action = state.legal_actions()[0]
        if action > 51:
          # TODO(ed2k) extend beyond just bidding
          action = ai_action(state, net, params)
        state.apply_action(action)
      else:
        result = bots[state.current_player() // 2].step(state)
        state.apply_action(result)
  return state

