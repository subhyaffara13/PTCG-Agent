
def _stateful_to_state_dict(state_dict: STATE_DICT_TYPE) -> STATE_DICT_TYPE:
    """Creates a shallow copy of `state_dict` where `state_dict` is called for each Stateful object."""
    stateful_state_dict = {}
    for key, elem in state_dict.items():
        # Apply _dcp_method_logger to each state_dict() call
        def _elem_to_state_dict(elem):
            return elem.state_dict() if isinstance(elem, Stateful) else elem

        _elem_to_state_dict.__name__ = f"_stateful_to_state_dict.{key}"

        stateful_state_dict[key] = _dcp_method_logger(log_exceptions=True)(
            _elem_to_state_dict
        )(elem)
    return stateful_state_dict

