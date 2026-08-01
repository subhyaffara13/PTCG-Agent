
def model_signature(model: torch.nn.Module | Callable) -> inspect.Signature:
    return inspect.signature(
        model.forward if isinstance(model, torch.nn.Module) else model
    )

