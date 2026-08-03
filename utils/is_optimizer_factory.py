from typing import Any

def is_optimizer_factory(optimizer_cls_or_factory: Any) -> bool:
    """
    Check if the returned value from a handler is a factory rather than an Optimizer class.

    Factory callables are used for complex optimizers like Muon or Dion that need to:
    - Split parameters between multiple internal optimizers
    - Handle complex sharding logic
    - Access the full model structure for parameter grouping

    Args:
        optimizer_cls_or_factory: The first element returned by an optimizer handler.

    Returns:
        `bool`: True if it's not an Optimizer class (i.e., likely a factory), False if it's an Optimizer class.
    """
    # If it's a class that's a subclass of torch.optim.Optimizer, it's not a factory
    if isinstance(optimizer_cls_or_factory, type) and issubclass(optimizer_cls_or_factory, torch.optim.Optimizer):
        return False
    return True

