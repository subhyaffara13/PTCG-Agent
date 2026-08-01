
def remove_proxy_from_state_dict(state_dict: dict, in_place: bool) -> dict:
    """
    If `in_place` is false, return a new copy of `state_dict` with "proxy" removed from `v.__dict__`.
    `v` is the values in the dictionary.
    If `in_place` is true, modify `state_dict` in place.
    """
    if in_place:
        for k, v in state_dict.items():
            if hasattr(v, "proxy"):
                delattr(state_dict[k], "proxy")
        return state_dict
    else:
        new_state_dict = {}
        for k, v in state_dict.items():
            if hasattr(v, "proxy"):
                new_state_dict[k] = v.detach().clone()
            else:
                new_state_dict[k] = v
        return new_state_dict

