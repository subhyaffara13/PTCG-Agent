
def _create_empty_mfg_state(game: dynamic_routing.DynamicRoutingGame):
  """Create an empty MFG state for the N player routing game.

  Args:
    game: the N player game.

  Returns:
    new_mfg_state: an empty MFG state corresponding to the N player game.
  """
  od_demand_dict = {}
  for vehicle in game._vehicles:  # pylint:disable=protected-access
    key = (vehicle.origin, vehicle.destination, vehicle.departure_time)
    if key not in od_demand_dict:
      od_demand_dict[key] = 0
    od_demand_dict[key] += 1
  od_demand = []
  for (origin, destination, departure_time), counts in od_demand_dict.items():
    od_demand.append(
        dynamic_routing_utils.OriginDestinationDemand(origin, destination,
                                                      departure_time, counts))
  return mean_field_routing_game.MeanFieldRoutingGame(
      {
          "max_num_time_step": game.max_game_length(),
          "time_step_length": game.time_step_length
      },
      network=game.network,
      od_demand=od_demand,
      perform_sanity_checks=game.perform_sanity_checks).new_initial_state()

