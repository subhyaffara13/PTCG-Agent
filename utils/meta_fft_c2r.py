
def meta_fft_c2r(self: Tensor, dim: list[int], normalization: int, lastdim: int):
    # _fft_c2r_mkl
    torch._check(self.dtype.is_complex)

    if device_hint(self) == "cuda":
        out_sizes = list(self.size())
        out_sizes[dim[-1]] = lastdim

        output = self.new_empty(out_sizes, dtype=toRealValueType(self.dtype))

        if use_optimized_cufft_path(dim):
            return _exec_fft(
                output,
                self.clone(memory_format=torch.contiguous_format),
                out_sizes,
                dim,
                forward=False,
            )
        else:
            # First complete any C2C transforms
            if len(dim) > 1:
                temp = meta_fft_c2c(self, dim[:-1], 0, forward=False)
            else:
                temp = self.clone(memory_format=torch.contiguous_format)
            return _exec_fft(output, temp, out_sizes, [dim[-1]], forward=False)

    elif torch.backends.mkl.is_available():
        # _fft_c2r_mkl in aten/src/ATen/native/mkl/SpectralOps.cpp
        input = self
        if len(dim) > 1:
            c2c_dims = dim[:-1]
            input = meta_fft_c2c(self, c2c_dims, normalization, forward=False)
            dim = dim[-1:]

        out_sizes = list(input.size())
        out_sizes[dim[-1]] = lastdim
        out = self.new_empty(out_sizes, dtype=toRealValueType(self.dtype))
        return _exec_fft(out, input, out_sizes, dim, forward=False)

    else:
        out_sizes = list(self.size())
        out_sizes[dim[-1]] = lastdim
        return self.new_empty(out_sizes, dtype=toRealValueType(self.dtype))

