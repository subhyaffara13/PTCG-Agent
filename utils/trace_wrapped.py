
def trace_wrapped(*args: Any, **kwargs: Any) -> Any:
    with torch.no_grad():
        return _trace_wrapped_op(*args, **kwargs)

