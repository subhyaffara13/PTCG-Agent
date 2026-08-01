
def _make_fft_harness(name,
                      *,
                      shape=(14, 15, 16, 17),
                      dtype=np.float32,
                      fft_type=lax.FftType.FFT,
                      fft_lengths=(17,)):

  def _fft_rng_factory(dtype):
    _all_integers = (
        jtu.dtypes.all_integer + jtu.dtypes.all_unsigned + jtu.dtypes.boolean)
    # For integer types, use small values to keep the errors small
    if dtype in _all_integers:
      return jtu.rand_small
    else:
      return jtu.rand_default

  define(
      lax.fft_p,
      f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_ffttype={fft_type}_fftlengths={fft_lengths}",
      lambda *args: lax.fft_p.bind(
          args[0], fft_type=args[1], fft_lengths=args[2]),
      [RandArg(shape, dtype),
       StaticArg(fft_type),
       StaticArg(fft_lengths)],
      rng_factory=_fft_rng_factory(dtype),
      shape=shape,
      dtype=dtype,
      fft_type=fft_type,
      fft_lengths=fft_lengths)

