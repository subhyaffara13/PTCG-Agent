
def _get_attr(self, name):
    # stop recursive pickling
    return getattr(self, name, None) or getattr(__builtin__, name)


def _get_attr(model: torch.nn.Module, attr_name: str):
    return _get_attr_via_attr_list(model, attr_name.split("."))

