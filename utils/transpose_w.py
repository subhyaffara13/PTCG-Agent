
def transpose_w(W: _T, trans_w: bool) -> _T:
    """
    Transpose W based on the trans_w flag.
    """
    if isinstance(W, ir.IRNode):
        if trans_w:
            if not isinstance(W, ir.TensorBox):
                # pyrefly: ignore [bad-assignment]
                W = ir.TensorBox(W)
            W = L.permute(W, [1, 0])
    else:
        if trans_w:
            assert isinstance(W, torch.Tensor)
            # pyrefly: ignore [bad-assignment]
            W = W.transpose(0, 1)
    # pyrefly: ignore [bad-return]
    return W

