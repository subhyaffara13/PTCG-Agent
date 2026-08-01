
def validate_unique_levels(levels: list[Index]) -> None:
    for level in levels:
        if not level.is_unique:
            raise ValueError(f"Level values not unique: {level.tolist()}")

