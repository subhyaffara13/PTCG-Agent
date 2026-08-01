
def _fetch_dims(tree: dict | list | tuple | torch.Tensor) -> list[tuple[int, ...]]:
    shapes = []
    if isinstance(tree, dict):
        for v in tree.values():
            shapes.extend(_fetch_dims(v))
    elif isinstance(tree, (list, tuple)):
        for t in tree:
            shapes.extend(_fetch_dims(t))
    elif isinstance(tree, torch.Tensor):
        shapes.append(tree.shape)
    else:
        raise TypeError("Not supported")

    return shapes

