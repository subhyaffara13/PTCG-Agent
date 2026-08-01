
def _check_stack_inputs(tensors: TensorSequenceType) -> None:
    from torch.fx.experimental.symbolic_shapes import sym_eq

    entry_shape = tensors[0].shape
    for i in range(1, len(tensors)):
        torch._check(
            sym_eq(tensors[i].shape, entry_shape),
            lambda: f"stack expects each tensor to be equal size, but got {entry_shape} at entry 0 ",
        )

