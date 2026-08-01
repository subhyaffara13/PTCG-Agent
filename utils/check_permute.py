
def check_permute(node: torch.fx.Node) -> bool:
    ranks = len(node.meta["tensor_meta"].shape)
    if len(node.args) > 3:
        permutation = [node.args[i] % ranks for i in range(1, ranks + 1)]  # type: ignore[operator]
    elif (
        "permutation" in node.kwargs
        and node.kwargs["permutation"] is not None
        and len(node.kwargs["permutation"]) > 2  # type: ignore[arg-type]
    ):
        permutation = [i % ranks for i in node.kwargs["permutation"]]  # type: ignore[operator, union-attr]
    else:
        return False
    allowed_permutation = list(range(ranks))
    allowed_permutation[-1] = ranks - 2
    allowed_permutation[-2] = ranks - 1
    return permutation == allowed_permutation

