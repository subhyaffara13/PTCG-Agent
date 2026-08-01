
def last_predictions(agent):
  if hasattr(agent, "last_predictions"):
    return agent.last_predictions()
  else:
    return np.zeros(pyspiel.ROSHAMBO_NUM_BOTS)

