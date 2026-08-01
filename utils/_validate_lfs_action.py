
def _validate_lfs_action(lfs_action: dict):
    """validates response from the LFS batch endpoint"""
    if not (
        isinstance(lfs_action.get("href"), str)
        and (lfs_action.get("header") is None or isinstance(lfs_action.get("header"), dict))
    ):
        raise ValueError("lfs_action is improperly formatted")
    return lfs_action

