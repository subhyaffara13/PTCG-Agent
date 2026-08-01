
def _state_to_str(x, y, t, population, player_id):
  """A string that uniquely identify (pos, t, population, player_id)."""
  if int(player_id) >= 0:
    return f"(pop={population}, t={t}, pos=[{x} {y}])"
  if player_id == pyspiel.PlayerId.MEAN_FIELD:
    return f"(pop={population}, t={t}_a, pos=[{x} {y}])"
  if player_id == pyspiel.PlayerId.CHANCE:
    return f"(pop={population}, t={t}_a_mu, pos=[{x} {y}])"


def _state_to_str(
    is_chance_init: bool,
    location: str,
    time_step: int,
    player_id: int,
    waiting_time: int,
    destination: str,
    final_arrival_time: float,
) -> str:
  """Convert the state to a string representation.

  As the string representation will be used in dictionaries for various
  algorithms that computes the state value, expected return, best response or
  find the mean field Nash equilibrium.
  The state is uniquely define by the current time, the type of node
  (decision, mean field or chance), the vehicle location, its destination and
  its waiting time.
  Args:
    is_chance_init: True if at chance initialization.
    location: the location of the representative player.
    time_step: the current time step.
    player_id: the current node type as a player id.
    waiting_time: the representative player waiting time.
    destination: the destination of the representative player.
    final_arrival_time: time of arrival.

  Returns:
    state_string: string representing uniquely the mean field game.
  """
  if is_chance_init:
    return "initial chance node"
  if player_id == pyspiel.PlayerId.DEFAULT_PLAYER_ID:
    time = str(time_step)
  elif player_id == pyspiel.PlayerId.MEAN_FIELD:
    time = f"{time_step}_mean_field"
  elif player_id == pyspiel.PlayerId.CHANCE:
    time = f"{time_step}_chance"
  else:
    raise ValueError(
        "Player id should be DEFAULT_PLAYER_ID, MEAN_FIELD or CHANCE")
  if final_arrival_time:
    return (f"Arrived at {location}, with arrival time "
            f"{final_arrival_time}, t={time}")
  return (f"Location={location}, waiting_time={waiting_time},"
          f" t={time}, destination='{destination}'")


def _state_to_str(x, t, player_id):
  """A string that uniquely identifies (x, t, player_id)."""
  if int(player_id) == pyspiel.PlayerId.DEFAULT_PLAYER_ID:
    return f"(t={t}, pos={x})"
  if player_id == pyspiel.PlayerId.MEAN_FIELD:
    return f"(t={t}_a, pos={x})"
  if player_id == pyspiel.PlayerId.CHANCE:
    return f"(t={t}_a_mu, pos={x})"


def _state_to_str(x, y, t, population, player_id):
  """A string that uniquely identify (pos, t, population, player_id)."""
  if int(player_id) >= 0:
    return f"(pop={population}, t={t}, pos=[{x} {y}])"
  if player_id == pyspiel.PlayerId.MEAN_FIELD:
    return f"(pop={population}, t={t}_a, pos=[{x} {y}])"
  if player_id == pyspiel.PlayerId.CHANCE:
    return f"(pop={population}, t={t}_a_mu, pos=[{x} {y}])"

