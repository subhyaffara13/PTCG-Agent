
def _check_torch_fn(node: torch.fx.Node) -> None:
    torch_fn = node.meta.get("torch_fn")
    if torch_fn is None:
        raise SpecViolationError(
            f"Unable to find torch_fn metadata for node {node.name}"
        )
    if (
        not isinstance(torch_fn, tuple)
        and isinstance(torch_fn[0], str)
        and isinstance(torch_fn[1], str)
    ):
        raise SpecViolationError(
            f"Node.meta {node.name} has invalid torch_fn field {torch_fn}"
        )

