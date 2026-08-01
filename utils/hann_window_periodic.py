
def hann_window_periodic(
    window_length: int,
    periodic: bool = True,
    *,
    dtype: torch.dtype | None = None,
    layout: torch.layout | None = None,
    device: torch.device | None = None,
    pin_memory: bool | None = None,
) -> Tensor:
    r"""hann_window(window_length, periodic=True, *, dtype=None, layout=None, device=None, pin_memory=False) -> Tensor

    Returns a Hann window of size :attr:`window_length`.

    .. math::
        w[n] = 0.5 - 0.5 \cos\!\left(\frac{2\pi n}{N-1}\right)

    where :math:`N` is ``window_length + 1`` when ``periodic=True`` (for spectral analysis),
    or ``window_length`` when ``periodic=False`` (symmetric window).

    Low-precision dtypes (``bfloat16``, ``float16``) are computed in ``float32`` then cast.

    Args:
        window_length (int): the size of returned window.
        periodic (bool, optional): if ``True``, returns a periodic window for use with STFT.
            Default: ``True``.

    Keyword args:
        dtype (:class:`torch.dtype`, optional): desired dtype. Default: global default.
        layout (:class:`torch.layout`, optional): desired layout. Default: ``torch.strided``.
        device (:class:`torch.device`, optional): desired device. Default: current device.
        pin_memory (bool, optional): if ``True``, pins the returned tensor. Default: ``False``.
    """
    dtype = dtype if dtype is not None else torch.get_default_dtype()
    if window_length == 0:
        return torch.empty(
            (0,), dtype=dtype, layout=layout, device=device, pin_memory=pin_memory
        )
    if window_length == 1:
        return torch.ones(
            (1,), dtype=dtype, layout=layout, device=device, pin_memory=pin_memory
        )
    compute_dtype = utils.get_computation_dtype(dtype)
    n = window_length + 1 if periodic else window_length
    t = torch.arange(
        n,
        dtype=compute_dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
    )
    t = t * (2.0 * torch.pi / (n - 1))
    t = torch.cos(t)
    t = t * -0.5 + 0.5
    window = t.narrow(0, 0, window_length) if periodic else t
    return window.to(dtype)

