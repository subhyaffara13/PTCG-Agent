
def should_optimize_getattr_on_nn_module(value: Any) -> bool:
    return isinstance(value, torch.nn.Module)

