
def _bool_to_status(changed: bool) -> PropagateStatus:
    """
    Return the variant of the success flag depending on whether there is any change.
    """
    return (
        PropagateStatus.SUCCEED_WITH_CHANGE
        if changed
        else PropagateStatus.SUCCEED_NO_CHANGE
    )

