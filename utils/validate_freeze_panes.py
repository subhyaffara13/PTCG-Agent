
def validate_freeze_panes(freeze_panes: tuple[int, int]) -> Literal[True]: ...


def validate_freeze_panes(freeze_panes: None) -> Literal[False]: ...


def validate_freeze_panes(freeze_panes: tuple[int, int] | None) -> bool:
    if freeze_panes is not None:
        if len(freeze_panes) == 2 and all(
            isinstance(item, int) for item in freeze_panes
        ):
            return True

        raise ValueError(
            "freeze_panes must be of form (row, column) "
            "where row and column are integers"
        )

    # freeze_panes wasn't specified, return False so it won't be applied
    # to output sheet
    return False

