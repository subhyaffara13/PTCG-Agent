
def _unique_state_dict(module, keep_vars=False):
    # since Parameter.detach() always creates a new torch.Tensor instance,
    # id(v) doesn't work with it. So we always get the Parameter or Buffer
    # as values, and deduplicate the params using Parameters and Buffers
    state_dict = module.state_dict(keep_vars=True)
    filtered_dict = type(state_dict)()
    seen_ids: set[int] = set()
    for k, v in state_dict.items():
        if id(v) in seen_ids:
            continue
        seen_ids.add(id(v))
        if keep_vars:
            filtered_dict[k] = v
        else:
            filtered_dict[k] = v.detach()
    return filtered_dict

