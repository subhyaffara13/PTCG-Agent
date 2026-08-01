
def _ops_filter_safe(name: str) -> bool:
    """
    An ops filter which allows pickle-safe ops. Pickle-safe ops are built-in
    ones where it will be possible to unpickle on any machine which has PyTorch.
    """
    # TODO: This list is pretty pessimistic right now. What's the full list?
    return name.startswith(
        (
            "torch.ops.aten",
            "torch.ops.fbgemm",
        )
    )

