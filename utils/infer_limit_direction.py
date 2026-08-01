
def infer_limit_direction(
    limit_direction: Literal["backward", "forward", "both"] | None, method: str
) -> Literal["backward", "forward", "both"]:
    # Set `limit_direction` depending on `method`
    if limit_direction is None:
        if method in ("backfill", "bfill"):
            limit_direction = "backward"
        else:
            limit_direction = "forward"
    else:
        if method in ("pad", "ffill") and limit_direction != "forward":
            raise ValueError(
                f"`limit_direction` must be 'forward' for method `{method}`"
            )
        if method in ("backfill", "bfill") and limit_direction != "backward":
            raise ValueError(
                f"`limit_direction` must be 'backward' for method `{method}`"
            )
    return limit_direction

