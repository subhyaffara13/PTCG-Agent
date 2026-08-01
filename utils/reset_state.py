
def reset_state():
    """
    Returns a context manager that resets all state once exited.

    See Also
    --------
    set_state
        Context manager that sets the backend state.
    get_state
        Gets a state to be set by this context manager.
    """
    with set_state(get_state()):
        yield

