
def create_games(origin,
                 destination,
                 num_vehicles,
                 graph,
                 max_time_step,
                 time_step_length=1.0,
                 departure_time=None):
  if departure_time is not None:
    raise NotImplementedError("To do.")
  list_of_vehicles = [
      dynamic_routing_utils.Vehicle(origin, destination)
      for _ in range(num_vehicles)
  ]
  game = dynamic_routing.DynamicRoutingGame(
      {
          "max_num_time_step": max_time_step,
          "time_step_length": time_step_length
      },
      network=graph,
      vehicles=list_of_vehicles)
  seq_game = pyspiel.convert_to_turn_based(game)
  od_demand = [
      dynamic_routing_utils.OriginDestinationDemand(origin, destination, 0,
                                                    num_vehicles)
  ]
  mfg_game = mean_field_routing_game.MeanFieldRoutingGame(
      {
          "max_num_time_step": max_time_step,
          "time_step_length": time_step_length
      },
      network=graph,
      od_demand=od_demand)
  return game, seq_game, mfg_game

