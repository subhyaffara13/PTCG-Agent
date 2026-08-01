
def unique_graph_name_with_root(
    root: torch.fx.GraphModule, prefix: str
) -> tuple[int, str]:
    next_name = None
    i = 0
    # pyrefly: ignore [bad-assignment]
    while not next_name:
        candidate = f"{prefix}_{i}"
        if hasattr(root, candidate):
            i += 1
        else:
            next_name = candidate
    return i, next_name

