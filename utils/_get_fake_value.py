from typing import Union

def _get_fake_value(x: Union[VariableTracker, Proxy, "FakeTensor"]) -> "FakeTensor":
    if isinstance(x, variables.VariableTracker):
        return x.as_proxy().node.meta["example_value"]
    elif isinstance(x, torch.fx.Proxy):
        return x.node.meta["example_value"]
    else:
        return x

