
def _del_attr(model: torch.nn.Module, attr_name: str):
    attr_names = attr_name.split(".")
    t = _get_attr_via_attr_list(model, attr_names[:-1])
    return delattr(t, attr_names[-1])

