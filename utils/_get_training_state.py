
def _get_training_state(
    handle: FlatParamHandle,
) -> HandleTrainingState:
    """Returns the training state of the handles in ``handle``."""
    _p_assert(handle, "Expects a non-empty handle")
    return handle._training_state

