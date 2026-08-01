
def _is_valid_qlinear_lowering_pattern():
    def fn(match):
        if len(match.nodes) != 1:
            return False
        return match.nodes[0].target in (
            torch.ops.onednn.qlinear_pointwise.default,
            torch.ops.onednn.qlinear_pointwise.tensor,
            torch.ops.onednn.qlinear_pointwise.binary,
            torch.ops.onednn.qlinear_pointwise.binary_tensor,
        )

    return fn

