
def _dropout_returns_masked_input_and_mask(
    g: jit_utils.GraphContext, input: torch._C.Value, p: float, train: bool
) -> tuple[torch._C.Value, torch._C.Value | None]:
    symbolic_helper.check_training_mode(train, "dropout")
    # In eval mode, dropout is non-op. That is, if the node's
    # train param is set to False, dropout just returns its inputs.
    if not train:
        return input, None
    p = g.op("Constant", value_t=torch.tensor(p))
    t = g.op("Constant", value_t=torch.tensor(train, dtype=torch.bool))
    r, mask = g.op("Dropout", input, p, t, outputs=2)
    return r, mask

