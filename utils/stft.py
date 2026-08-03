import itertools
import time

def stft(
    input: Tensor,
    n_fft: int,
    hop_length: int | None = None,
    win_length: int | None = None,
    window: Tensor | None = None,
    center: bool = True,
    pad_mode: str = "reflect",
    normalized: bool = False,
    onesided: bool | None = None,
    return_complex: bool | None = None,
    align_to_window: bool | None = None,
) -> Tensor:
    r"""Short-time Fourier transform (STFT).

    .. warning::
        From version 1.8.0, :attr:`return_complex` must always be given
        explicitly for real inputs and `return_complex=False` has been
        deprecated. Strongly prefer `return_complex=True` as in a future
        pytorch release, this function will only return complex tensors.

        Note that :func:`torch.view_as_real` can be used to recover a real
        tensor with an extra last dimension for real and imaginary components.

    .. warning::
        From version 2.1, a warning will be provided if a :attr:`window` is
        not specified. In a future release, this attribute will be required.
        Not providing a window currently defaults to using a rectangular window,
        which may result in undesirable artifacts. Consider using tapered windows,
        such as :func:`torch.hann_window`.

    The STFT computes the Fourier transform of short overlapping windows of the
    input. This giving frequency components of the signal as they change over
    time. The interface of this function is modeled after (but *not* a drop-in
    replacement for) librosa_ stft function.

    .. _librosa: https://librosa.org/doc/latest/generated/librosa.stft.html

    Ignoring the optional batch dimension, this method computes the following
    expression:

    .. math::
        X[\omega, m] = \sum_{k = 0}^{\text{win\_length-1}}%
                            \text{window}[k]\ \text{input}[m \times \text{hop\_length} + k]\ %
                            \exp\left(- j \frac{2 \pi \cdot \omega k}{\text{n\_fft}}\right),

    where :math:`m` is the index of the sliding window, and :math:`\omega` is
    the frequency :math:`0 \leq \omega < \text{n\_fft}` for ``onesided=False``,
    or :math:`0 \leq \omega < \lfloor \text{n\_fft} / 2 \rfloor + 1` for ``onesided=True``.

    * :attr:`input` must be either a 1-D time sequence or a 2-D batch of time
      sequences.

    * If :attr:`hop_length` is ``None`` (default), it is treated as equal to
      ``floor(n_fft / 4)``.

    * If :attr:`win_length` is ``None`` (default), it is treated as equal to
      :attr:`n_fft`.

    * :attr:`window` can be a 1-D tensor of size :attr:`win_length`, e.g., from
      :meth:`torch.hann_window`. If :attr:`window` is ``None`` (default), it is
      treated as if having :math:`1` everywhere in the window. If
      :math:`\text{win\_length} < \text{n\_fft}`, :attr:`window` will be padded on
      both sides to length :attr:`n_fft` before being applied.

    * If :attr:`center` is ``True`` (default), :attr:`input` will be padded on
      both sides so that the :math:`t`-th frame is centered at time
      :math:`t \times \text{hop\_length}`. Otherwise, the :math:`t`-th frame
      begins at time  :math:`t \times \text{hop\_length}`.

    * :attr:`pad_mode` determines the padding method used on :attr:`input` when
      :attr:`center` is ``True``. See :meth:`torch.nn.functional.pad` for
      all available options. Default is ``"reflect"``.

    * If :attr:`onesided` is ``True`` (default for real input), only values for
      :math:`\omega` in :math:`\left[0, 1, 2, \dots, \left\lfloor
      \frac{\text{n\_fft}}{2} \right\rfloor + 1\right]` are returned because
      the real-to-complex Fourier transform satisfies the conjugate symmetry,
      i.e., :math:`X[m, \omega] = X[m, \text{n\_fft} - \omega]^*`.
      Note if the input or window tensors are complex, then :attr:`onesided`
      output is not possible.

    * If :attr:`normalized` is ``True`` (default is ``False``), the function
      returns the normalized STFT results, i.e., multiplied by :math:`(\text{frame\_length})^{-0.5}`.

    * If :attr:`return_complex` is ``True`` (default if input is complex), the
      return is a ``input.dim() + 1`` dimensional complex tensor. If ``False``,
      the output is a ``input.dim() + 2`` dimensional real tensor where the last
      dimension represents the real and imaginary components.

    Returns either a complex tensor of size :math:`(* \times N \times T)` if
    :attr:`return_complex` is true, or a real tensor of size :math:`(* \times N
    \times T \times 2)`. Where :math:`*` is the optional batch size of
    :attr:`input`, :math:`N` is the number of frequencies where STFT is applied
    and :math:`T` is the total number of frames used.

    .. warning::
      This function changed signature at version 0.4.1. Calling with the
      previous signature may cause error or return incorrect result.

    Args:
        input (Tensor): the input tensor of shape `(B?, L)` where `B?` is an optional
            batch dimension
        n_fft (int): size of Fourier transform
        hop_length (int, optional): the distance between neighboring sliding window
            frames. Default: ``None`` (treated as equal to ``floor(n_fft / 4)``)
        win_length (int, optional): the size of window frame and STFT filter.
            Default: ``None``  (treated as equal to :attr:`n_fft`)
        window (Tensor, optional): the optional window function.
            Shape must be 1d and `<= n_fft`
            Default: ``None`` (treated as window of all :math:`1` s)
        center (bool, optional): whether to pad :attr:`input` on both sides so
            that the :math:`t`-th frame is centered at time :math:`t \times \text{hop\_length}`.
            Default: ``True``
        pad_mode (str, optional): controls the padding method used when
            :attr:`center` is ``True``. Default: ``"reflect"``
        normalized (bool, optional): controls whether to return the normalized STFT results
             Default: ``False``
        onesided (bool, optional): controls whether to return half of results to
            avoid redundancy for real inputs.
            Default: ``True`` for real :attr:`input` and :attr:`window`, ``False`` otherwise.
        return_complex (bool, optional): whether to return a complex tensor, or
            a real tensor with an extra last dimension for the real and
            imaginary components.

            .. versionchanged:: 2.0
               ``return_complex`` is now a required argument for real inputs,
               as the default is being transitioned to ``True``.

            .. deprecated:: 2.0
               ``return_complex=False`` is deprecated, instead use ``return_complex=True``
               Note that calling :func:`torch.view_as_real` on the output will
               recover the deprecated output format.

    Returns:
        Tensor: A tensor containing the STFT result with shape `(B?, N, T, C?)` where
           - `B?` is an optional batch dimension from the input.
           - `N` is the number of frequency samples, `(n_fft // 2) + 1` for
             `onesided=True`, or otherwise `n_fft`.
           - `T` is the number of frames, `1 + L // hop_length`
             for `center=True`, or `1 + (L - n_fft) // hop_length` otherwise.
           - `C?` is an optional length-2 dimension of real and imaginary
             components, present when `return_complex=False`.

    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            stft,
            (input,),
            input,
            n_fft,
            hop_length=hop_length,
            win_length=win_length,
            window=window,
            center=center,
            pad_mode=pad_mode,
            normalized=normalized,
            onesided=onesided,
            return_complex=return_complex,
            align_to_window=align_to_window,
        )
    if center and align_to_window is not None:
        raise RuntimeError(
            "stft align_to_window should only be set when center = false"
        )
    # NOTE: Do not edit. This code will be removed once the forward-compatibility
    #       period is over for PR #73432
    if center:
        signal_dim = input.dim()
        extended_shape = [1] * (3 - signal_dim) + list(input.size())
        pad = int(n_fft // 2)
        input = F.pad(input.view(extended_shape), [pad, pad], pad_mode)
        input = input.view(input.shape[-signal_dim:])
    return _VF.stft(  # type: ignore[attr-defined]
        input,
        n_fft,
        hop_length,
        win_length,
        window,
        normalized,
        onesided,
        return_complex,
        align_to_window,
    )


def stft(
    input: Tensor,
    n_fft: int,
    hop_length: int | None = None,
    win_length: int | None = None,
    window: Tensor | None = None,
    center: bool = True,
    pad_mode: str = "reflect",
    normalized: bool = False,
    onesided: bool | None = None,
    return_complex: bool | None = None,
    align_to_window: bool | None = None,
) -> Tensor:
    torch._check(
        window is None or window.device == input.device,
        lambda: (
            f"stft input and window must be on the same device but got self on {input.device}"
            + f" and window on {window.device}"  # type: ignore[union-attr]
        ),
    )
    torch._check(
        not center or align_to_window is None,
        lambda: "stft only supports align_to_window for center = False.",
    )

    hop_length_ = hop_length if hop_length is not None else n_fft // 4
    win_length_ = win_length if win_length is not None else n_fft

    if return_complex is None:
        return_complex_ = input.is_complex() or (
            window is not None and utils.is_complex_dtype(window.dtype)
        )
        torch._check(
            return_complex_,
            lambda: (
                "stft requires the return_complex parameter be given for real inputs, "
                + "and will further require that return_complex=True in a future PyTorch release."
            ),
        )
    else:
        return_complex_ = return_complex

    torch._check(
        utils.is_float_dtype(input.dtype) or utils.is_complex_dtype(input.dtype),
        lambda: "stft expected a tensor of floating point or complex values",
    )
    torch._check(1 <= input.ndim <= 2, lambda: "stft expected a 1D or 2D tensor")

    original_ndim = input.ndim
    if original_ndim == 1:
        input = input.unsqueeze(0)

    if center:
        extra_dims = 3 - input.ndim
        pad_amount = n_fft // 2
        extended_shape = [*itertools.repeat(1, extra_dims), *input.shape]
        input = aten.pad(input.view(extended_shape), [pad_amount, pad_amount], pad_mode)
        input = input.view(input.size()[extra_dims:])

    length = input.size(1)
    torch._check(
        0 < n_fft <= length,
        lambda: f"stft expected 0 < n_fft <= {length}, but got n_fft={n_fft}",
    )
    torch._check(
        hop_length_ > 0,
        lambda: f"stft expected hop_length > 0 but got hop_length={hop_length_}",
    )
    torch._check(
        0 < win_length_ <= n_fft,
        lambda: f"stft expected 0 < win_length <= n_fft but got win_length={win_length_}",
    )
    torch._check(
        window is None or window.shape == (win_length_,),
        lambda: (
            f"expected a 1D window tensor of size equal to win_length={win_length_}, "
            + f"but got window with size {window.shape}"  # type: ignore[union-attr]
        ),
    )

    if win_length_ < n_fft:
        if window is None:
            window = torch.ones(win_length_, dtype=input.dtype, device=input.device)
        left = (n_fft - win_length_) // 2
        window = aten.constant_pad_nd(window, [left, n_fft - win_length_ - left])

    if not center and align_to_window:
        input_pad_amount = (n_fft - win_length_) // 2
        input = aten.pad(input, [input_pad_amount, input_pad_amount], pad_mode)

    input = input.unfold(dimension=-1, size=n_fft, step=hop_length_)

    if window is not None:
        input = input * window

    complex_fft = utils.is_complex_dtype(input.dtype)
    onesided = onesided if onesided is not None else not complex_fft
    norm = "ortho" if normalized else None
    if onesided:
        torch._check(
            not complex_fft,
            lambda: "Cannot have onesided output if window or input is complex",
        )
        out = torch.fft.rfft(input, dim=-1, norm=norm)
    else:
        out = torch.fft.fft(input, dim=-1, norm=norm)

    out.transpose_(1, 2)

    if original_ndim == 1:
        out = out.squeeze_(0)

    return out if return_complex_ else torch.view_as_real(out)


def stft(
    g: jit_utils.GraphContext,
    input: _C.Value,
    n_fft: int,
    hop_length: int | None = None,
    win_length: int | None = None,
    window: _C.Value | None = None,
    normalized: bool = False,
    onesided: bool | None = True,
    return_complex: bool | None = False,
    align_to_window: bool | None = None,
) -> _C.Value:
    """Associates `torch.stft` with the `STFT` ONNX operator.
    Note that torch.stft calls _VF.stft, without centering or padding options.
    Hence, this function does not contain these two arguments.
    See torch.stft source code for more info.

    Args:
        g: Graph to write the ONNX representation into
        input: Input tensor for the transformation
        n_fft: FFT size
        hop_length: Size of the hop. Defaults to `floot(n_fft // 4)`
        win_length: Size of the analysis window. Defaults to `n_fft`
        window: Analysis window. Defaults to a window of all ones
        normalized: Whether to return a normalized STFT
        onesided: Whether to return only half (+1) of the results, given the
            symmetry of the STFT
        return_complex: Whether to return the complex value (Note: Must be
            `False` or `None`)

    Returns:
        op: Operator for torch.stft associated with STFT (ONNX)
    """
    # Checks
    if return_complex:
        raise errors.SymbolicValueError(
            msg="STFT does not currently support complex types", value=input
        )

    if align_to_window is not None:
        raise errors.SymbolicValueError(
            msg="STFT does not currently support the align_to_window option",
            value=input,
        )  # TODO(#145944): add compatibility with align_to_window option.

    # Get STFT sizes
    frame_step_value = hop_length if hop_length is not None else n_fft // 4
    frame_step_const = g.op(
        "Constant", value_t=torch.tensor(frame_step_value, dtype=torch.int64)
    )
    frame_length_const = g.op(
        "Constant", value_t=torch.tensor(n_fft, dtype=torch.int64)
    )

    # Pre-process input if needed
    signal = input
    signal_rank = symbolic_helper._get_tensor_rank(signal)
    if signal_rank == 1:
        # Add batch dimension
        signal = g.op(
            "Unsqueeze",
            signal,
            g.op("Constant", value_t=torch.tensor([0], dtype=torch.int64)),
        )
    elif signal_rank is None or signal_rank > 2:
        raise errors.SymbolicValueError(
            msg="STFT can only take inputs of 1 [signal] or 2 [batch, signal] dimensions. "
            f"Current rank of signal is {signal_rank}, please reduce it.",
            value=input,
        )

    # Get window and make sure it's the same size as `win_length` or `n_fft`
    # pyrefly: ignore [bad-argument-type]
    n_win = symbolic_helper._get_tensor_dim_size(window, dim=0)
    if n_win is not None:
        win_length_default = win_length if win_length else n_fft
        if n_win != win_length_default:
            raise AssertionError(
                "Analysis window size must equal `win_length` or `n_fft`. "
                f"Please, set `win_length` or `n_fft` to match `window` size ({n_win})"
            )

        # Center window around zeros if needed (required by ONNX's STFT)
        if n_win < n_fft:
            left, right = _compute_edge_sizes(n_fft, n_win)
            left_win = g.op("Constant", value_t=torch.zeros(left))
            right_win = g.op("Constant", value_t=torch.zeros(right))
            # pyrefly: ignore [bad-argument-type]
            window = g.op("Concat", left_win, window, right_win, axis_i=0)

    # Create window, if needed
    if symbolic_helper._is_none(window):
        if win_length:
            if win_length > n_fft:
                raise errors.SymbolicValueError(
                    msg="The analysis window can't be longer than the size of the FFT. "
                    f"Please set `win_length` ({win_length}) to `n_fft` ({n_fft}) or less.",
                    value=input,
                )

            # Center window, if needed
            left, right = _compute_edge_sizes(n_fft, win_length)
            torch_window = torch.hstack(
                (torch.zeros(left), torch.ones(win_length), torch.zeros(right))
            )
        else:
            # Rectangle window
            torch_window = torch.ones(n_fft)
        if torch_window.shape[0] != n_fft:
            raise AssertionError(
                f"torch_window.shape[0]={torch_window.shape[0]} != n_fft={n_fft}"
            )
        window = g.op("Constant", value_t=torch_window)
    window = g.op(
        "Cast",
        # pyrefly: ignore [bad-argument-type]
        window,
        to_i=_type_utils.JitScalarType.from_value(signal).onnx_type(),
    )

    # Run STFT
    result = g.op(
        "STFT",
        signal,
        frame_step_const,
        window,
        frame_length_const,
        onesided_i=1 if onesided is None or onesided else 0,
    )

    # Transpose to mimic torch.stft's behavior
    result = g.op("Transpose", result, perm_i=[0, 2, 1, 3])

    # Remove batch dimension, if needed
    if signal_rank == 1:
        result = g.op(
            "Squeeze",
            result,
            g.op("Constant", value_t=torch.tensor([0], dtype=torch.int64)),
        )

    # Normalize, if needed
    if normalized:
        sqrt_nfft = torch.sqrt(torch.tensor(n_fft, dtype=signal.type().dtype()))
        result = g.op("Div", result, g.op("Constant", value_t=sqrt_nfft))

    return result


def stft(x, fs=1.0, window='hann_periodic', nperseg=256, noverlap=None, nfft=None,
         detrend=False, return_onesided=True, boundary='zeros', padded=True,
         axis=-1, scaling='spectrum'):
    r"""Compute the Short Time Fourier Transform (legacy function).

    STFTs can be used as a way of quantifying the change of a
    nonstationary signal's frequency and phase content over time.

    .. legacy:: function

        `ShortTimeFFT` is a newer STFT / ISTFT implementation with more
        features. A :ref:`comparison <tutorial_stft_legacy_stft>` between the
        implementations can be found in the :ref:`tutorial_stft` section of the
        :ref:`user_guide`.

    Parameters
    ----------
    x : array_like
        Time series of measurement values
    fs : float, optional
        Sampling frequency of the `x` time series. Defaults to 1.0.
    window : str or tuple or array_like, optional
        Desired window to use. If `window` is a string or tuple, it is
        passed to `get_window` to generate the window values, which are
        DFT-even by default. See `get_window` for a list of windows and
        required parameters. If `window` is array_like it will be used
        directly as the window and its length must be nperseg. Defaults
        to a periodic Hann window.
    nperseg : int, optional
        Length of each segment. Defaults to 256.
    noverlap : int, optional
        Number of points to overlap between segments. If `None`,
        ``noverlap = nperseg // 2``. Defaults to `None`. When
        specified, the COLA constraint must be met (see Notes below).
    nfft : int, optional
        Length of the FFT used, if a zero padded FFT is desired. If
        `None`, the FFT length is `nperseg`. Defaults to `None`.
    detrend : str or function or `False`, optional
        Specifies how to detrend each segment. If `detrend` is a
        string, it is passed as the `type` argument to the `detrend`
        function. If it is a function, it takes a segment and returns a
        detrended segment. If `detrend` is `False`, no detrending is
        done. Defaults to `False`.
    return_onesided : bool, optional
        If `True`, return a one-sided spectrum for real data. If
        `False` return a two-sided spectrum. Defaults to `True`, but for
        complex data, a two-sided spectrum is always returned.
    boundary : str or None, optional
        Specifies whether the input signal is extended at both ends, and
        how to generate the new values, in order to center the first
        windowed segment on the first input point. This has the benefit
        of enabling reconstruction of the first input point when the
        employed window function starts at zero. Valid options are
        ``['even', 'odd', 'constant', 'zeros', None]``. Defaults to
        'zeros', for zero padding extension. I.e. ``[1, 2, 3, 4]`` is
        extended to ``[0, 1, 2, 3, 4, 0]`` for ``nperseg=3``.
    padded : bool, optional
        Specifies whether the input signal is zero-padded at the end to
        make the signal fit exactly into an integer number of window
        segments, so that all of the signal is included in the output.
        Defaults to `True`. Padding occurs after boundary extension, if
        `boundary` is not `None`, and `padded` is `True`, as is the
        default.
    axis : int, optional
        Axis along which the STFT is computed; the default is over the
        last axis (i.e. ``axis=-1``).
    scaling : {'spectrum', 'psd'}
        The default 'spectrum' scaling allows each frequency line of `Zxx` to
        be interpreted as a magnitude spectrum. The 'psd' option scales each
        line to a power spectral density - it allows to calculate the signal's
        energy by numerically integrating over ``abs(Zxx)**2``.

        .. versionadded:: 1.9.0

    Returns
    -------
    f : ndarray
        Array of sample frequencies.
    t : ndarray
        Array of segment times.
    Zxx : ndarray
        STFT of `x`. By default, the last axis of `Zxx` corresponds
        to the segment times.

    See Also
    --------
    istft: Inverse Short Time Fourier Transform
    ShortTimeFFT: Newer STFT/ISTFT implementation providing more features.
    check_COLA: Check whether the Constant OverLap Add (COLA) constraint
                is met
    check_NOLA: Check whether the Nonzero Overlap Add (NOLA) constraint is met
    welch: Power spectral density by Welch's method.
    spectrogram: Spectrogram by Welch's method.
    csd: Cross spectral density by Welch's method.
    lombscargle: Lomb-Scargle periodogram for unevenly sampled data

    Notes
    -----
    In order to enable inversion of an STFT via the inverse STFT in
    `istft`, the signal windowing must obey the constraint of "Nonzero
    OverLap Add" (NOLA), and the input signal must have complete
    windowing coverage (i.e. ``(x.shape[axis] - nperseg) %
    (nperseg-noverlap) == 0``). The `padded` argument may be used to
    accomplish this.

    Given a time-domain signal :math:`x[n]`, a window :math:`w[n]`, and a hop
    size :math:`H` = `nperseg - noverlap`, the windowed frame at time index
    :math:`t` is given by

    .. math:: x_{t}[n]=x[n]w[n-tH]

    The overlap-add (OLA) reconstruction equation is given by

    .. math:: x[n]=\frac{\sum_{t}x_{t}[n]w[n-tH]}{\sum_{t}w^{2}[n-tH]}

    The NOLA constraint ensures that every normalization term that appears
    in the denominator of the OLA reconstruction equation is nonzero. Whether a
    choice of `window`, `nperseg`, and `noverlap` satisfy this constraint can
    be tested with `check_NOLA`.


    .. versionadded:: 0.19.0

    References
    ----------
    .. [1] Oppenheim, Alan V., Ronald W. Schafer, John R. Buck
           "Discrete-Time Signal Processing", Prentice Hall, 1999.
    .. [2] Daniel W. Griffin, Jae S. Lim "Signal Estimation from
           Modified Short-Time Fourier Transform", IEEE 1984,
           10.1109/TASSP.1984.1164317

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    >>> rng = np.random.default_rng()

    Generate a test signal, a 2 Vrms sine wave whose frequency is slowly
    modulated around 3kHz, corrupted by white noise of exponentially
    decreasing magnitude sampled at 10 kHz.

    >>> fs = 10e3
    >>> N = 1e5
    >>> amp = 2 * np.sqrt(2)
    >>> noise_power = 0.01 * fs / 2
    >>> time = np.arange(N) / float(fs)
    >>> mod = 500*np.cos(2*np.pi*0.25*time)
    >>> carrier = amp * np.sin(2*np.pi*3e3*time + mod)
    >>> noise = rng.normal(scale=np.sqrt(noise_power),
    ...                    size=time.shape)
    >>> noise *= np.exp(-time/5)
    >>> x = carrier + noise

    Compute and plot the STFT's magnitude.

    >>> f, t, Zxx = signal.stft(x, fs, nperseg=1000)
    >>> plt.pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=amp, shading='gouraud')
    >>> plt.title('STFT Magnitude')
    >>> plt.ylabel('Frequency [Hz]')
    >>> plt.xlabel('Time [sec]')
    >>> plt.show()

    Compare the energy of the signal `x` with the energy of its STFT:

    >>> E_x = sum(x**2) / fs  # Energy of x
    >>> # Calculate a two-sided STFT with PSD scaling:
    >>> f, t, Zxx = signal.stft(x, fs, nperseg=1000, return_onesided=False,
    ...                         scaling='psd')
    >>> # Integrate numerically over abs(Zxx)**2:
    >>> df, dt = f[1] - f[0], t[1] - t[0]
    >>> E_Zxx = sum(np.sum(Zxx.real**2 + Zxx.imag**2, axis=0) * df) * dt
    >>> # The energy is the same, but the numerical errors are quite large:
    >>> np.isclose(E_x, E_Zxx, rtol=1e-2)
    True

    """
    if scaling == 'psd':
        scaling = 'density'
    elif scaling != 'spectrum':
        raise ValueError(f"Parameter {scaling=} not in ['spectrum', 'psd']!")

    freqs, time, Zxx = _spectral_helper(x, x, fs, window, nperseg, noverlap,
                                        nfft, detrend, return_onesided,
                                        scaling=scaling, axis=axis,
                                        mode='stft', boundary=boundary,
                                        padded=padded)

    return freqs, time, Zxx


def stft(x: Array, fs: ArrayLike = 1.0, window: str = 'hann', nperseg: int = 256,
         noverlap: int | None = None, nfft: int | None = None,
         detrend: bool = False, return_onesided: bool = True, boundary: str | None = 'zeros',
         padded: bool = True, axis: int = -1) -> tuple[Array, Array, Array]:
  """
  Compute the short-time Fourier transform (STFT).

  JAX implementation of :func:`scipy.signal.stft`.

  Args:
    x: Array representing a time series of input values.
    fs: Sampling frequency of the time series (default: 1.0).
    window: Data tapering window to apply to each segment. Can be a window function name,
      a tuple specifying a window length and function, or an array (default: ``'hann'``).
    nperseg: Length of each segment (default: 256).
    noverlap: Number of points to overlap between segments (default: ``nperseg // 2``).
    nfft: Length of the FFT used, if a zero-padded FFT is desired. If ``None`` (default),
      the FFT length is ``nperseg``.
    detrend: Specifies how to detrend each segment. Can be ``False`` (default: no detrending),
      ``'constant'`` (remove mean), ``'linear'`` (remove linear trend), or a callable
      accepting a segment and returning a detrended segment.
    return_onesided: If True (default), return a one-sided spectrum for real inputs.
      If False, return a two-sided spectrum.
    boundary: Specifies whether the input signal is extended at both ends, and how.
      Options are ``None`` (no extension), ``'zeros'`` (default), ``'even'``, ``'odd'``,
      or ``'constant'``.
    padded: Specifies whether the input signal is zero-padded at the end to make its
      length a multiple of `nperseg`. If True (default), the padded signal length is
      the next multiple of ``nperseg``.
    axis: Axis along which the STFT is computed; the default is over the last axis (-1).

  Returns:
    A length-3 tuple of arrays ``(f, t, Zxx)``. ``f`` is the Array of sample frequencies.
    ``t`` is the Array of segment times, and ``Zxx`` is the STFT of ``x``.

  See Also:
    :func:`jax.scipy.signal.istft`: inverse short-time Fourier transform.
  """
  return _spectral_helper(x, None, fs, window, nperseg, noverlap,
                          nfft, detrend, return_onesided,
                          scaling='spectrum', axis=axis,
                          mode='stft', boundary=boundary,
                          padded=padded)

