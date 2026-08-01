
def _should_warn(outer_attr: str, inner_attr: str, user_set_attributes: set | None) -> bool:
    """Determine if we should raise a warning for the combination `outer_attr` and `inner_attr`, based on whether
    they were provided explicitly, i.e. if they were in `user_set_attributes`.
    For example, if `outer_attr="do_sample"`, the warnings should be suppressed for `inner_attr` flags (e.g. "top_p") that weren't
    explicitly set by the caller. When `do_sample=False` is explicitly required by the user, values such as `top_p` inherited
    from a model's `generation_config.json` are harmless when the user opts for greedy decoding.
    """
    outer_sample_set = user_set_attributes is not None and outer_attr in user_set_attributes
    inner_attr_set = user_set_attributes is not None and inner_attr in user_set_attributes
    # We should warn only if both are explicitly set, none are set, or only the inner_attr is set while outer_attr is not
    return (
        (outer_sample_set and inner_attr_set)
        or (not outer_sample_set and not inner_attr_set)
        or (inner_attr_set and not outer_sample_set)
    )

