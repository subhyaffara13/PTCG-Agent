
def _fight_battle(planet, arriving_fleets):
    """Resolve battle on a planet. Mirrors PlanetState::FightBattle in
    game.cpp lines 74-117.

    `planet` is mutated in place. `arriving_fleets` is the subset of fleets
    whose turns_remaining == 0 and dest == planet.id.
    """
    forces = {}  # owner -> ships
    forces[planet[3]] = forces.get(planet[3], 0) + planet[4]
    for f in arriving_fleets:
        forces[f[0]] = forces.get(f[0], 0) + f[1]

    # Top two by ship count using the original strict-greater walk so the
    # tie semantics line up with the C++ engine: a tie at the top leaves
    # the planet's prior owner intact with zero ships.
    winner_owner, winner_ships = 0, 0
    second_ships = 0
    for owner, ships in forces.items():
        if ships > second_ships:
            if ships > winner_ships:
                second_ships = winner_ships
                winner_owner, winner_ships = owner, ships
            else:
                second_ships = ships

    if winner_ships > second_ships:
        planet[3] = winner_owner
        planet[4] = winner_ships - second_ships
    else:
        planet[4] = 0

