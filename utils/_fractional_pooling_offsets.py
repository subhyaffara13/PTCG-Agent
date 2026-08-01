
def _fractional_pooling_offsets(samples, in_sz, out_sz, kernel_sz, dim, ndims):
    out_sz = out_sz[dim]
    in_sz = in_sz[dim]
    kernel_sz = kernel_sz[dim]
    samples_loader = samples.make_loader()

    def load(prefix, i):
        # Handle indexing for samples tensor correctly for different input dimensions
        # samples tensor always has shape (N, C, 2) for fractional_max_pool2d where:
        # - N=1 for 3D inputs (C,H,W), N=batch_size for 4D inputs (N,C,H,W)
        # - C=num_channels
        # - 2 for the two spatial dimensions (height, width)
        samples_shape = samples.get_size()

        if len(samples_shape) == 3:  # Expected: (N, C, 2)
            if len(prefix) == 1:
                # 3D input case: prefix=(channel,), samples=(1, C, 2)
                # Access: samples[0, channel, dim]
                sample = samples_loader([0, prefix[0], ndims - 1 - dim])
            elif len(prefix) >= 2:
                # 4D+ input case: prefix=(batch, channel, ...), samples=(batch, C, 2)
                # Access: samples[batch, channel, dim]
                sample = samples_loader([prefix[0], prefix[1], ndims - 1 - dim])
            else:
                # Edge case - shouldn't happen for valid fractional pooling
                sample = samples_loader([0, 0, ndims - 1 - dim])
        else:
            # Fallback for unexpected tensor shapes
            sample = samples_loader([*prefix, ndims - 1 - dim])
        i_expr = ops.index_expr(i, samples.get_dtype())
        diff = ops.index_expr(in_sz - kernel_sz, torch.int64)
        out_sz_expr = ops.index_expr(out_sz - 1, torch.int64)
        alpha = ops.truediv(
            ops.to_dtype(diff, torch.float64), ops.to_dtype(out_sz_expr, torch.float64)
        )
        alpha = ops.where(ops.eq(out_sz_expr, 0), 0, alpha)
        seq_i = ops.trunc((i_expr + sample) * alpha) - ops.trunc(sample * alpha)
        seq_i = ops.to_dtype(seq_i, torch.int64)
        mask = ops.lt(i_expr, out_sz_expr)
        return ops.indirect_indexing(ops.where(mask, seq_i, diff), sympy.sympify(in_sz))

    return load

