
def _load_packed_weight(
    self,
    state_dict,
    prefix,
    local_metadata,
    strict,
    missing_keys,
    unexpected_keys,
    error_msgs,
):
    attrs_to_pop = []
    for attr_name in state_dict:
        if attr_name.startswith("_packed_weight") and isinstance(
            state_dict[attr_name], torch._C.ScriptObject
        ):  # type: ignore[attr-defined] # noqa: B950
            setattr(self, attr_name, state_dict[attr_name])
            attrs_to_pop.append(attr_name)

    # pop the packed param attributesn
    for attr_name in attrs_to_pop:
        state_dict.pop(attr_name)

