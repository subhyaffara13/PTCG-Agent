
def _fft_lowering_gpu(ctx, x, *, fft_type, fft_lengths):
  # Decompose multi-dimensional IRFFT into a sequence of transforms.
  # cuFFT assumes Hermitian symmetry on all dimensions of a multi-dimensional
  # C2R transform, whereas our other implementations and NumPy only require
  # symmetry on the final dimension.
  if fft_type == FftType.IRFFT and len(fft_lengths) > 1:
    rank = len(ctx.avals_in[0].shape)

    # Move the final C2R axis (at index -1) to the start of the FFT block.
    target_pos = rank - len(fft_lengths)

    perm_out = list(range(rank))
    perm_out.insert(target_pos, perm_out.pop(-1))
    x = hlo.transpose(x, mlir.dense_int_array(perm_out))

    # Apply multi-dimensional IFFT on the outer axes (which are now at the end).
    outer_lengths = fft_lengths[:-1]
    x = hlo.fft(
        x,
        hlo.FftTypeAttr.get(FftType.IFFT.name),
        mlir.dense_int_array(outer_lengths),
    )

    # Move the C2R axis back to the end.
    perm_in = list(range(rank))
    perm_in.append(perm_in.pop(target_pos))
    x = hlo.transpose(x, mlir.dense_int_array(perm_in))

    # Apply 1D IRFFT on the last axis.
    x = hlo.fft(
        x,
        hlo.FftTypeAttr.get(FftType.IRFFT.name),
        mlir.dense_int_array((fft_lengths[-1],)),
    )

    return [x]

  return _fft_lowering(ctx, x, fft_type=fft_type, fft_lengths=fft_lengths)

