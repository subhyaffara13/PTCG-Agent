
def _unsqueeze_multiple(x: TensorLikeType, dimensions: list[int]) -> TensorLikeType:
    for dim in sorted(dimensions):
        x = torch.unsqueeze(x, dim)
    return x

