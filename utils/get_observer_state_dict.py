
def get_observer_state_dict(mod):
    r"""
    Returns the state dict corresponding to the observer stats.
    Traverse the model state_dict and extract out the stats.
    """
    od = OrderedDict()
    if isinstance(mod, torch.jit.RecursiveScriptModule):
        for k, v in mod.state_dict().items():
            if "observer" in k:
                od[k] = v
    else:
        # path for GraphModule and nn.Module (eager mode)
        for k, v in mod.state_dict().items():
            if "activation_post_process" in k:
                od[k] = v
    od._metadata = mod.state_dict()._metadata  # type: ignore[attr-defined]
    return od

