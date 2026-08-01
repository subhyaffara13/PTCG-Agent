
def attacker_agent(board):
    me = board.current_player
    remaining_kore = me.kore
    shipyards = me.shipyards
    size = board.configuration.size
    spawn_cost = board.configuration.spawn_cost
    # randomize shipyard order
    shipyards = sample(shipyards, len(shipyards))
    for idx, shipyard in enumerate(shipyards):
        closest_enemy_shipyard = get_closest_enemy_shipyard(board, shipyard.position, me)
        if closest_enemy_shipyard and (remaining_kore >= spawn_cost or shipyard.ship_count >= 50):
            if shipyard.ship_count >= 50:
                flight_plan = get_shortest_flight_path_between(shipyard.position, closest_enemy_shipyard.position, size)
                shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(50, flight_plan)
            elif remaining_kore >= spawn_cost:
                shipyard.next_action = ShipyardAction.spawn_ships(
                    min(shipyard.max_spawn, int(remaining_kore / spawn_cost))
                )
        elif shipyard.ship_count >= 21:
            best_h = 0
            best_gap1 = 5
            best_gap2 = 5
            start_dir = board.step % 4
            dirs = Direction.list_directions()[start_dir:] + Direction.list_directions()[:start_dir]
            for gap1 in range(0, 10):
                for gap2 in range(0, 10):
                    h = check_path(board, shipyard.position, dirs, gap1, gap2, 0.2)
                    if h > best_h:
                        best_h = h
                        best_gap1 = gap1
                        best_gap2 = gap2
            gap1 = str(best_gap1)
            gap2 = str(best_gap2)
            flight_plan = Direction.list_directions()[start_dir].to_char()
            if int(gap1):
                flight_plan += gap1
            next_dir = (start_dir + 1) % 4
            flight_plan += Direction.list_directions()[next_dir].to_char()
            if int(gap2):
                flight_plan += gap2
            next_dir = (next_dir + 1) % 4
            flight_plan += Direction.list_directions()[next_dir].to_char()
            if int(gap1):
                flight_plan += gap1
            next_dir = (next_dir + 1) % 4
            flight_plan += Direction.list_directions()[next_dir].to_char()
            shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(21, flight_plan)
        elif shipyard.ship_count > 0 and len(shipyards) > 1:
            flight_plan = get_shortest_flight_path_between(
                shipyard.position, shipyards[(idx + 1) % len(shipyards)].position, size
            )
            shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(shipyard.ship_count, flight_plan)

