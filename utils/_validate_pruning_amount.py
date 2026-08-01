
def _validate_pruning_amount(amount, tensor_size) -> None:
    r"""Validate that the pruning amount is meaningful wrt to the size of the data.

    Validation helper to check that the amount of parameters to prune
    is meaningful wrt to the size of the data (`tensor_size`).

    Args:
        amount (int or float): quantity of parameters to prune.
            If float, should be between 0.0 and 1.0 and represent the
            fraction of parameters to prune. If int, it represents the
            absolute number of parameters to prune.
        tensor_size (int): absolute number of parameters in the tensor
            to prune.
    """
    # TODO: consider removing this check and allowing users to specify
    # a number of units to prune that is greater than the number of units
    # left to prune. In this case, the tensor will just be fully pruned.

    if isinstance(amount, numbers.Integral) and amount > tensor_size:
        raise ValueError(
            f"amount={amount} should be smaller than the number of parameters to prune={tensor_size}"
        )

