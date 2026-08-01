
def native_dropout(input: Tensor, p: float, train: bool | None):
    if train and p != 0:
        if p == 1:
            return (torch.zeros_like(input), torch.zeros_like(input, dtype=torch.bool))
        if not input.dtype.is_floating_point:
            raise RuntimeError(
                "result type Float can't be cast to the desired output type Long"
            )
        bool_mask = torch.rand_like(input) > p
        res = bool_mask * input * float(1.0 / (1.0 - p))
        return (res, bool_mask)
    else:
        return (input, torch.ones_like(input, dtype=torch.bool))


def native_dropout(x, p, train):
    if config.fallback_random:
        return pytree.tree_map(
            TensorBox.create,
            ir.FallbackKernel.create(aten.native_dropout.default, x, p, train),
        )
    else:
        raise AssertionError("should be handled in replace_random.py")


def native_dropout(g: jit_utils.GraphContext, input, p, train):
    return _dropout_returns_masked_input_and_mask(g, input, p, train)

