
def strict_mode_fake_tensor_mode(mode, callable, operands):
    with mode:
        true_outs = callable(*operands)
    return true_outs

