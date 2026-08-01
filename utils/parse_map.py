
def parse_map(text):
    """Parse a Planet Wars Point-in-Time map.

    Returns (planets, fleets) where each entry is the list shape used in
    observations. Mirrors Game::ParseGameState in game.cpp.
    """
    planets = []
    fleets = []
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        tokens = line.split()
        if tokens[0] == "P":
            if len(tokens) != 6:
                raise ValueError(f"invalid planet line: {raw_line!r}")
            x = float(tokens[1])
            y = float(tokens[2])
            owner = int(tokens[3])
            num_ships = int(tokens[4])
            growth_rate = int(tokens[5])
            planets.append([len(planets), x, y, owner, num_ships, growth_rate])
        elif tokens[0] == "F":
            if len(tokens) != 7:
                raise ValueError(f"invalid fleet line: {raw_line!r}")
            fleets.append(
                [
                    int(tokens[1]),  # owner
                    int(tokens[2]),  # num_ships
                    int(tokens[3]),  # source
                    int(tokens[4]),  # dest
                    int(tokens[5]),  # total_trip
                    int(tokens[6]),  # turns_remaining
                ]
            )
        else:
            raise ValueError(f"unknown map line: {raw_line!r}")
    return planets, fleets

