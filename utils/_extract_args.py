
def _extract_args(arg: Any) -> Any:
    if isinstance(arg, Node):
        return arg.meta.get("example_value")
    elif isinstance(arg, (torch.Tensor, int)):
        return arg
    else:
        return None

