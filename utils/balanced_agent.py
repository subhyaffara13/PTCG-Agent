
def balanced_agent(board):
    me = board.current_player
    me = board.current_player
    remaining_kore = me.kore
    shipyards = me.shipyards
    convert_cost = board.configuration.convert_cost
    size = board.configuration.size
    spawn_cost = board.configuration.spawn_cost

    # randomize shipyard order
    shipyards = sample(shipyards, len(shipyards))
    for shipyard in shipyards:
        closest_enemy_shipyard = get_closest_enemy_shipyard(board, shipyard.position, me)
        invading_fleet_size = 100
        dist_to_closest_enemy_shipyard = (
            100 if not closest_enemy_shipyard else shipyard.position.distance_to(closest_enemy_shipyard.position, size)
        )
        if (
            closest_enemy_shipyard
            and (closest_enemy_shipyard.ship_count < 20 or dist_to_closest_enemy_shipyard < 15)
            and (remaining_kore >= spawn_cost or shipyard.ship_count >= invading_fleet_size)
        ):
            if shipyard.ship_count >= invading_fleet_size:
                flight_plan = get_shortest_flight_path_between(shipyard.position, closest_enemy_shipyard.position, size)
                shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(invading_fleet_size, flight_plan)
            elif remaining_kore >= spawn_cost:
                shipyard.next_action = ShipyardAction.spawn_ships(
                    min(shipyard.max_spawn, int(remaining_kore / spawn_cost))
                )

        elif remaining_kore > 500 and shipyard.max_spawn > 5:
            if shipyard.ship_count >= convert_cost + 7:
                start_dir = randint(0, 3)
                next_dir = (start_dir + 1) % 4
                best_kore = 0
                best_gap1 = 0
                best_gap2 = 0
                for gap1 in range(5, 15, 3):
                    for gap2 in range(5, 15, 3):
                        gap2 = randint(3, 9)
                        diff1 = Direction.from_index(start_dir).to_point() * gap1
                        diff2 = Direction.from_index(next_dir).to_point() * gap2
                        diff = diff1 + diff2
                        pos = shipyard.position.translate(diff, board.configuration.size)
                        h = check_location(board, pos, me)
                        if h > best_kore:
                            best_kore = h
                            best_gap1 = gap1
                            best_gap2 = gap2
                gap1 = str(best_gap1)
                gap2 = str(best_gap2)
                flight_plan = Direction.list_directions()[start_dir].to_char() + gap1
                flight_plan += Direction.list_directions()[next_dir].to_char() + gap2
                flight_plan += "C"
                shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(
                    max(convert_cost + 7, int(shipyard.ship_count / 2)), flight_plan
                )
            elif remaining_kore >= spawn_cost:
                shipyard.next_action = ShipyardAction.spawn_ships(
                    min(shipyard.max_spawn, int(remaining_kore / spawn_cost))
                )

        # launch a large fleet if able
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
        # else spawn if possible
        elif remaining_kore > board.configuration.spawn_cost * shipyard.max_spawn:
            remaining_kore -= board.configuration.spawn_cost
            if remaining_kore >= spawn_cost:
                shipyard.next_action = ShipyardAction.spawn_ships(
                    min(shipyard.max_spawn, int(remaining_kore / spawn_cost))
                )

