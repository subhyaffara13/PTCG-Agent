
def cosine(
    M: int,
    *,
    sym: bool = True,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    device: torch.device | None = None,
    requires_grad: bool = False,
) -> Tensor:
    if dtype is None:
        dtype = torch.get_default_dtype()

    _window_function_checks("cosine", M, dtype, layout)

    if M == 0:
        return torch.empty(
            (0,), dtype=dtype, layout=layout, device=device, requires_grad=requires_grad
        )

    start = 0.5
    constant = torch.pi / (M + 1 if not sym and M > 1 else M)

    k = torch.linspace(
        start=start * constant,
        end=(start + (M - 1)) * constant,
        steps=M,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )

    return torch.sin(k)


def cosine(u, v, w=None):
    """
    Compute the Cosine distance between 1-D arrays.

    The Cosine distance between `u` and `v`, is defined as

    .. math::

        1 - \\frac{u \\cdot v}
                  {\\|u\\|_2 \\|v\\|_2}.

    where :math:`u \\cdot v` is the dot product of :math:`u` and
    :math:`v`.

    Parameters
    ----------
    u : (N,) array_like of floats
        Input array.
    v : (N,) array_like of floats
        Input array.
    w : (N,) array_like of floats, optional
        The weights for each value in `u` and `v`. Default is None,
        which gives each value a weight of 1.0

    Returns
    -------
    cosine : double
        The Cosine distance between vectors `u` and `v`.

    Examples
    --------
    >>> from scipy.spatial import distance
    >>> distance.cosine([1, 0, 0], [0, 1, 0])
    1.0
    >>> distance.cosine([100, 0, 0], [0, 1, 0])
    1.0
    >>> distance.cosine([1, 1, 0], [0, 1, 0])
    0.29289321881345254

    """
    # cosine distance is also referred to as 'uncentered correlation',
    #   or 'reflective correlation'
    return correlation(u, v, w=w, centered=False)


def cosine(M, sym=True, *, xp=None, device=None):
    """Return a window with a simple cosine shape.

    Parameters
    ----------
    M : int
        Number of points in the output window. If zero, an empty array
        is returned. An exception is thrown when it is negative.
    sym : bool, optional
        When True (default), generates a symmetric window, for use in filter
        design.
        When False, generates a periodic window, for use in spectral analysis.
    %(xp_device_snippet)s

    Returns
    -------
    w : ndarray
        The window, with the maximum value normalized to 1 (though the value 1
        does not appear if `M` is even and `sym` is True).

    Notes
    -----

    .. versionadded:: 0.13.0

    Examples
    --------
    Plot the window and its frequency response:

    >>> import numpy as np
    >>> from scipy import signal
    >>> from scipy.fft import fft, fftshift
    >>> import matplotlib.pyplot as plt

    >>> window = signal.windows.cosine(51)
    >>> plt.plot(window)
    >>> plt.title("Cosine window")
    >>> plt.ylabel("Amplitude")
    >>> plt.xlabel("Sample")

    >>> plt.figure()
    >>> A = fft(window, 2047) / (len(window)/2.0)
    >>> freq = np.linspace(-0.5, 0.5, len(A))
    >>> response = 20 * np.log10(np.abs(fftshift(A / abs(A).max())))
    >>> plt.plot(freq, response)
    >>> plt.axis([-0.5, 0.5, -120, 0])
    >>> plt.title("Frequency response of the cosine window")
    >>> plt.ylabel("Normalized magnitude [dB]")
    >>> plt.xlabel("Normalized frequency [cycles per sample]")
    >>> plt.show()

    """
    xp = _namespace(xp)

    if _len_guards(M):
        return xp.ones(M, dtype=xp.float64, device=device)
    M, needs_trunc = _extend(M, sym)

    w = xp.sin(xp.pi / M * (xp.arange(M, dtype=xp.float64, device=device) + .5))

    return _truncate(w, needs_trunc)


def cosine(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return CosineOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def cosine(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return CosineOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result

