
def _get_optional_value(litellm_params, optional_params, attribute_name):
    """Resolve Cisco optional params without inheriting sibling defaults."""
    if optional_params is not None:
        if isinstance(optional_params, dict):
            if attribute_name in optional_params:
                return optional_params[attribute_name]
        else:
            nested_fields_set = getattr(optional_params, "model_fields_set", None)
            if nested_fields_set is None or attribute_name in nested_fields_set:
                value = getattr(optional_params, attribute_name, None)
                if value is not None:
                    return value

    if litellm_params is None:
        return None
    # Only accept flattened values the caller explicitly set.
    fields_set = getattr(litellm_params, "model_fields_set", None)
    if fields_set is None or attribute_name not in fields_set:
        return None
    return getattr(litellm_params, attribute_name, None)

