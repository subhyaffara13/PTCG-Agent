from typing import Callable

def _fft_helper(x, win, detrend_func, nperseg, noverlap, nfft, sides):
    """
    Calculate windowed FFT, for internal use by
    `scipy.signal._spectral_helper`.

    .. legacy:: function

        This function is solely used by the legacy `_spectral_helper` function,
        which is located also in this file.

    This is a helper function that does the main FFT calculation for
    `_spectral helper`. All input validation is performed there, and the
    data axis is assumed to be the last axis of x. It is not designed to
    be called externally. The windows are not averaged over; the result
    from each window is returned.

    Returns
    -------
    result : ndarray
        Array of FFT data

    Notes
    -----
    Adapted from matplotlib.mlab

    .. versionadded:: 0.16.0
    """
    # Created sliding window view of array
    if nperseg == 1 and noverlap == 0:
        result = x[..., np.newaxis]
    else:
        step = nperseg - noverlap
        result = np.lib.stride_tricks.sliding_window_view(
            x, window_shape=nperseg, axis=-1, writeable=True
        )
        result = result[..., 0::step, :]

    # Detrend each data segment individually
    result = detrend_func(result)

    # Apply window by multiplication
    result = win * result

    # Perform the fft. Acts on last axis by default. Zero-pads automatically
    if sides == 'twosided':
        func = sp_fft.fft
    else:
        result = result.real
        func = sp_fft.rfft
    result = func(result, n=nfft)

    return result


def _fft_helper(x: Array, win: Array, detrend_func: Callable[[Array], Array],
                nperseg: int, noverlap: int, nfft: int | None, sides: str) -> Array:
  """Calculate windowed FFT in the same way the original SciPy does.
  """
  if x.dtype.kind == 'i':
    x = x.astype(win.dtype)

  *batch_shape, signal_length = x.shape
  # Created strided array of data segments
  if nperseg == 1 and noverlap == 0:
    result = x[..., np.newaxis]
  else:
    step = nperseg - noverlap
    starts = jnp.arange(signal_length - nperseg + 1, step=step)
    slice_func = partial(lax.dynamic_slice_in_dim, operand=x, slice_size=nperseg, axis=-1)
    result = api.vmap(slice_func, out_axes=-2)(start_index=starts)

  # Detrend each data segment individually
  result = detrend_func(result)

  # Apply window by multiplication
  if jnp.iscomplexobj(win):
    result, = promote_dtypes_complex(result)
  result = win.reshape((1,) * len(batch_shape) + (1, nperseg)) * result

  # Perform the fft on last axis. Zero-pads automatically
  if sides == 'twosided':
    return jnp_fft.fft(result, n=nfft)
  else:
    return jnp_fft.rfft(result.real, n=nfft)

