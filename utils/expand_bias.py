
def expand_bias(B: _T | None, X: _T) -> _T | None:
    """
    Expand Bias to the same size of X.
    """
    if B is not None:
        if isinstance(B, ir.IRNode):
            if not isinstance(B, ir.TensorBox):
                # pyrefly: ignore [bad-assignment]
                B = ir.TensorBox(B)
            assert hasattr(X, "get_size")
            # pyrefly: ignore [missing-attribute]
            B = L.expand(B, (X.get_size()[0], B.get_size()[-1]))
        else:
            assert isinstance(B, torch.Tensor)
            assert isinstance(X, torch.Tensor)
            # pyrefly: ignore [bad-assignment]
            B = B.expand(X.shape[0], B.shape[-1])
    return B

