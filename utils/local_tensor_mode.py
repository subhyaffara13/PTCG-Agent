
def local_tensor_mode() -> LocalTensorMode | None:
    """
    Returns the current active LocalTensorMode if one exists.

    This function checks the global stack of LocalTensorMode instance. If there
    is at least one LocalTensorMode active, it returns the most recently entered
    (top of the stack) LocalTensorMode. If no LocalTensorMode is active, it returns None.

    Returns:
        Optional[LocalTensorMode]: The current LocalTensorMode if active, else None.
    """
    local_tensor_mode_list = get_local_tensor_mode_list()
    if len(local_tensor_mode_list) > 0:
        return local_tensor_mode_list[-1]
    return None

