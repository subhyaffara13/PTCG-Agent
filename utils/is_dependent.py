
def is_dependent(constraint):
    """
    Checks if ``constraint`` is a ``_Dependent`` object.

    Args:
        constraint : A ``Constraint`` object.

    Returns:
        ``bool``: True if ``constraint`` can be refined to the type ``_Dependent``, False otherwise.

    Examples:
        >>> import torch
        >>> from torch.distributions import Bernoulli
        >>> from torch.distributions.constraints import is_dependent

        >>> dist = Bernoulli(probs=torch.tensor([0.6], requires_grad=True))
        >>> constraint1 = dist.arg_constraints["probs"]
        >>> constraint2 = dist.arg_constraints["logits"]

        >>> for constraint in [constraint1, constraint2]:
        >>>     if is_dependent(constraint):
        >>>         continue
    """
    return isinstance(constraint, _Dependent)

