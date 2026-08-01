
def validate_limit_area(limit_area: str | None) -> Literal["inside", "outside"] | None:
    if limit_area is not None:
        valid_limit_areas = ["inside", "outside"]
        limit_area = limit_area.lower()
        if limit_area not in valid_limit_areas:
            raise ValueError(
                f"Invalid limit_area: expecting one of {valid_limit_areas}, got "
                f"{limit_area}."
            )
    # error: Incompatible return value type (got "Optional[str]", expected
    # "Optional[Literal['inside', 'outside']]")
    return limit_area  # type: ignore[return-value]

