
def format_map(planets, fleets=()):
    """Serialise the current state into the Point-in-Time format."""
    lines = []
    for p in planets:
        lines.append(f"P {p[1]} {p[2]} {p[3]} {p[4]} {p[5]}")
    for f in fleets:
        lines.append(f"F {f[0]} {f[1]} {f[2]} {f[3]} {f[4]} {f[5]}")
    return "\n".join(lines)

