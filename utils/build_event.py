
def build_event(args: tuple[Any], kwargs: dict[Any, Any]) -> torch.Event:
    return torch._C.Event(*args, **kwargs)

