
def meta_repeat(self, repeats):
    torch._check(
        len(repeats) >= self.dim(),
        lambda: "Number of dimensions of repeat dims can not be smaller than number of dimensions of tensor",
    )
    for i, rep in enumerate(repeats):
        torch._check(
            rep >= 0,
            lambda: f"Repeats cannot be negative, found {rep} at index {i}",
        )
    # Add new leading dimensions to the tensor if the
    # number of target dimensions is larger than the
    # number of source dimensions.
    num_new_dimensions = len(repeats) - self.dim()
    padded_size = (1,) * num_new_dimensions + tuple(self.shape)
    target_size = [padded_size[i] * repeats[i] for i in range(len(repeats))]
    return self.new_empty(target_size)

