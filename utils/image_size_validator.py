
def image_size_validator(value: int | Sequence[int] | dict[str, int] | None = None):
    possible_keys = ["height", "width", "longest_edge", "shortest_edge", "max_height", "max_width"]
    if value is None:
        pass
    elif isinstance(value, dict) and any(k not in possible_keys for k in value.keys()):
        raise ValueError(f"Value for size must be a dict with keys {possible_keys} but got size={value}")

