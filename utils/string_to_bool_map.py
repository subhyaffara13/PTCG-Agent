
def string_to_bool_map(str_map: str) -> chex.Array:
    """Convert string map into boolean walking map."""
    bool_map = []
    for row in str_map.split("\n")[1:]:
        bool_map.append([r == " " for r in row])
    return jnp.array(bool_map)

