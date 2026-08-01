
def _fft_lowering(ctx, x, *, fft_type, fft_lengths):
  if not is_constant_shape(fft_lengths):
    # TODO: https://github.com/openxla/stablehlo/issues/1366
    raise NotImplementedError("Shape polymorphism for FFT with non-constant fft_length is not implemented for TPU and GPU")
  return [
      hlo.fft(
          x,
          hlo.FftTypeAttr.get(fft_type.name),
          mlir.dense_int_array(fft_lengths),
      )
  ]

