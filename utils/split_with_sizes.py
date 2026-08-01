
def split_with_sizes(x, sizes, dim=0):
    return split(x, sizes, dim)


def split_with_sizes(
    self: Tensor, split_sizes: list[int], dim: int = 0
) -> list[Tensor]:
    # NB: Perform the check_is_size tests first so that the
    # sum test does not try to do a replacement
    for i in range(len(split_sizes)):
        torch._check(
            split_sizes[i] >= 0,
            lambda: "split_with_sizes expects split_sizes have only non-negative entries",
        )
    torch._check_with(
        ValueError,
        builtins.sum(split_sizes) == self.shape[dim],
        lambda: f"Split sizes add up to {builtins.sum(split_sizes)} but got the tensor's size of {self.shape[dim]}",
    )

    splits = []
    offset = self.storage_offset()

    for split_size in split_sizes:
        new_shape = list(self.shape)
        new_shape[dim] = split_size
        # We reimplement narrow here to avoid a lot of checks in the
        # decomposition of narrow which calls slice_in_dim and slice
        splits.append(self.as_strided(new_shape, self.stride(), offset))
        offset = offset + self.stride()[dim] * split_size
    return splits


def split_with_sizes(g: jit_utils.GraphContext, self, split_sizes, dim, _outputs=None):
    return split(g, self, split_sizes, dim, _outputs)


def split_with_sizes(g: jit_utils.GraphContext, self, split_sizes, dim, _outputs=None):
    return split(g, self, split_sizes, dim, _outputs)


def split_with_sizes(g: jit_utils.GraphContext, self, split_sizes, dim, _outputs=None):
    if not symbolic_helper._is_split_static(split_sizes, _outputs):
        return symbolic_helper._onnx_opset_unsupported_detailed(
            "split_with_sizes", 9, 11, "Dynamic number of outputs not supported", self
        )
    # pyrefly: ignore [bad-argument-type]
    return g.op("Split", self, split_i=split_sizes, axis_i=dim, outputs=_outputs)

