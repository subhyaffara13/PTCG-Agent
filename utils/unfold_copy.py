
def unfold_copy(self: TensorLikeType, dimension: int, size: int, step: int):
    return self.unfold(dimension, size, step).clone(
        memory_format=torch.contiguous_format
    )

