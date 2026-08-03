import random
import math


def generate_map(seed):
    """Procedurally generate a symmetric Planet Wars map.

    Approximates the distribution produced by the original contest's
    map_generator_v2.py: 15-30 planets, point-symmetric or reflective
    symmetry, home planets at distance >= 4, all other planets at
    pairwise distance >= 2.

    Returns (planets, fleets) in the list-of-lists form used in
    observations.
    """
    rng = random.Random(seed)

    planets_to_generate = rng.randint(MIN_PLANETS, MAX_PLANETS)
    # symmetry_type: +1 = radial (point-symmetric, 180° rotation through
    # origin), -1 = linear (mirror across an axis). Radial requires an odd
    # total because the centre planet is unpaired.
    if rng.randint(0, 1):
        symmetry_type = 1
        if planets_to_generate % 2 == 0:
            planets_to_generate += 1
            if planets_to_generate > MAX_PLANETS:
                planets_to_generate = MIN_PLANETS + (MIN_PLANETS % 2 == 0)
    else:
        symmetry_type = -1

    # Internal "planet" records keep x/y in original-centred coordinates;
    # we translate them at the end. Shape matches the observation form
    # ([id, x, y, owner, ships, growth]) so validation helpers can reuse it.
    planets = []

    def add(x, y, owner, ships, growth):
        planets.append([len(planets), x, y, owner, ships, growth])

    # Centre planet at origin — always neutral, may have growth 0.
    add(0.0, 0.0, 0, rng.randint(MIN_SHIPS, MAX_SHIPS), rng.randint(0, MAX_GROWTH))
    planets_to_generate -= 1

    # Home planets.
    home1_x = home1_y = home2_x = home2_y = 0.0
    theta1 = theta2 = 0.0
    for _ in range(MAX_PLACEMENT_TRIES):
        r = _rand_radius(rng, MIN_DISTANCE, MAX_RADIUS)
        theta1 = rng.uniform(0, 360)
        if symmetry_type == 1:
            theta2 = theta1 + 180 if theta1 < 180 else theta1 - 180
        else:
            theta2 = rng.uniform(0, 360)
        home1_x, home1_y = _polar(r, theta1)
        home2_x, home2_y = _polar(r, theta2)
        if _pair_invalid(home1_x, home1_y, home2_x, home2_y, planets):
            continue
        if math.ceil(math.hypot(home1_x - home2_x, home1_y - home2_y)) < MIN_STARTING_DISTANCE:
            continue
        break
    else:
        raise RuntimeError(f"generate_map: failed to place home planets in {MAX_PLACEMENT_TRIES} tries (seed={seed})")
    add(home1_x, home1_y, 1, HOME_SHIPS, HOME_GROWTH)
    add(home2_x, home2_y, 2, HOME_SHIPS, HOME_GROWTH)
    planets_to_generate -= 2

    # Central neutrals — placed along the symmetry axis, equidistant from
    # both home planets.
    if symmetry_type == 1:
        no_central = 2 * rng.randint(0, MAX_CENTRAL // 2)
        theta_a = (theta1 + theta2) / 2
        theta_b = theta_a + 180
        for _ in range(no_central // 2):
            ships = rng.randint(MIN_SHIPS, MAX_SHIPS)
            growth = rng.randint(MIN_GROWTH, MAX_GROWTH)
            for _try in range(MAX_PLACEMENT_TRIES):
                r = _rand_radius(rng, MIN_DISTANCE, MAX_RADIUS)
                ax, ay = _polar(r, theta_a)
                bx, by = _polar(r, theta_b)
                if not _pair_invalid(ax, ay, bx, by, planets):
                    break
            else:
                raise RuntimeError(f"generate_map: failed to place central neutral pair in {MAX_PLACEMENT_TRIES} tries (seed={seed})")
            add(ax, ay, 0, ships, growth)
            add(bx, by, 0, ships, growth)
            planets_to_generate -= 2
    else:
        # Linear symmetry: central neutrals sit on the perpendicular
        # bisector. The remaining count must be even (pairs of mirrored
        # neutrals); pick `no_central` accordingly so we end up even.
        min_central = planets_to_generate % 2
        no_central = rng.randrange(min_central, MAX_CENTRAL + 1, 2)
        theta = (theta1 + theta2) / 2
        if rng.randint(0, 1) == 1:
            theta += 180
        for _ in range(no_central):
            ships = rng.randint(MIN_SHIPS, MAX_SHIPS)
            growth = rng.randint(MIN_GROWTH, MAX_GROWTH)
            for _try in range(MAX_PLACEMENT_TRIES):
                r = _rand_radius(rng, 0, MAX_RADIUS)
                x, y = _polar(r, theta)
                if not _too_close_or_ambiguous(x, y, planets):
                    actual = math.hypot(x, y)
                    if abs(actual - round(actual)) >= EPSILON:
                        break
            else:
                raise RuntimeError(f"generate_map: failed to place linear-axis neutral in {MAX_PLACEMENT_TRIES} tries (seed={seed})")
            add(x, y, 0, ships, growth)
            planets_to_generate -= 1

    # Remaining symmetric pairs of neutrals.
    assert planets_to_generate % 2 == 0, "odd remainder after central neutrals"
    home_distance = math.ceil(math.hypot(home1_x - home2_x, home1_y - home2_y))
    for i in range(planets_to_generate // 2):
        if i == 0:
            # Cap the first pair's ship count so neutrals near home planets
            # aren't unconquerable in the early game.
            cap = min(MAX_SHIPS, 5 * home_distance - 1)
            cap = max(cap, MIN_SHIPS)
            ships = rng.randint(MIN_SHIPS, cap)
        else:
            ships = rng.randint(MIN_SHIPS, MAX_SHIPS)
        growth = rng.randint(MIN_GROWTH, MAX_GROWTH)
        for _try in range(MAX_PLACEMENT_TRIES):
            r = _rand_radius(rng, MIN_DISTANCE, MAX_RADIUS)
            delta = rng.uniform(0, 360)
            ax, ay = _polar(r, theta1 + delta)
            bx, by = _polar(r, theta2 + symmetry_type * delta)
            if not _pair_invalid(ax, ay, bx, by, planets):
                break
        else:
            raise RuntimeError(f"generate_map: failed to place symmetric neutral pair in {MAX_PLACEMENT_TRIES} tries (seed={seed})")
        add(ax, ay, 0, ships, growth)
        add(bx, by, 0, ships, growth)

    # Translate so all coordinates are non-negative.
    for p in planets:
        p[1] += MAX_RADIUS
        p[2] += MAX_RADIUS

    return planets, []

