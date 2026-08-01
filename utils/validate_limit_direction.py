
def validate_limit_direction(
    limit_direction: str,
) -> Literal["forward", "backward", "both"]:
    valid_limit_directions = ["forward", "backward", "both"]
    limit_direction = limit_direction.lower()
    if limit_direction not in valid_limit_directions:
        raise ValueError(
            "Invalid limit_direction: expecting one of "
            f"{valid_limit_directions}, got '{limit_direction}'."
        )
    # error: Incompatible return value type (got "str", expected
    # "Literal['forward', 'backward', 'both']")
    return limit_direction  # type: ignore[return-value]

