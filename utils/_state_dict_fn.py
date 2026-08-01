
def _state_dict_fn(obj: nn.Module | torch.optim.Optimizer, api: str) -> Callable:
    call = getattr(obj, api)
    if call in _patched_state_dict:
        call = functools.partial(getattr(obj.__class__, api), self=obj)
    return call

