
def _upsample_get_cubic_coefficients(t: Tensor) -> TensorSequenceType:
    A = -0.75

    if t.device == torch.device("cpu"):
        tt1 = torch.stack([t, 1.0 - t], dim=0)
        tt2 = torch.stack([t + 1.0, 2.0 - t], dim=0)
        w03 = _upsample_cubic_convolution2(tt2, A)
        w12 = _upsample_cubic_convolution1(tt1, A)
        w0, w3 = torch.unbind(w03, dim=0)
        w1, w2 = torch.unbind(w12, dim=0)
        return w0, w1, w2, w3
    else:
        return (
            _upsample_cubic_convolution2(t + 1.0, A),
            _upsample_cubic_convolution1(t, A),
            _upsample_cubic_convolution1(1.0 - t, A),
            _upsample_cubic_convolution2(2.0 - t, A),
        )

