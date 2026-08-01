
def _fractional_max_pool(x, kernel_size, output_size, random_samples, n_dim):
    x.realize_hint()
    batch, inp_dhw = x.shape[:-n_dim], x.shape[-n_dim:]

    with config.patch(unroll_reductions_threshold=25):
        dhw_index_fn = [
            _fractional_pooling_offsets(
                samples=random_samples,
                in_sz=inp_dhw,
                out_sz=output_size,
                kernel_sz=kernel_size,
                ndims=n_dim,
                dim=d,
            )
            for d in range(n_dim)
        ]

        x_loader = x.make_loader()

        def fn_inner(idx, reduction_idx):
            prefix = idx[:-n_dim]
            return x_loader([*prefix, *increments_to_index(idx, reduction_idx)])

        def increments_to_index(idx, reduction_idx):
            prefix = idx[:-n_dim]
            bdhw = idx[-n_dim:]
            return [
                dhw_index_fn[d](prefix, bdhw[d]) + reduction_idx[d]
                for d in range(n_dim)
            ]

        new_size = list(batch) + list(output_size)
        dtype = x.get_dtype()
        result = Reduction.create(
            reduction_type="max",
            input_node=x,
            device=x.get_device(),
            dst_dtype=dtype,
            src_dtype=dtype,
            inner_fn=fn_inner,
            ranges=new_size,
            reduction_ranges=kernel_size,
        )
        offsets = Reduction.create(
            reduction_type="argmax",
            input_node=x,
            device=x.get_device(),
            dst_dtype=torch.int64,
            src_dtype=dtype,
            inner_fn=fn_inner,
            ranges=new_size,
            reduction_ranges=kernel_size,
        )
        assert isinstance(result, TensorBox), result
        if isinstance(result.data.data, Reduction):  # type: ignore[attr-defined]
            # Only realize if reduction isn't unrolled
            result.realize()
        assert isinstance(offsets, TensorBox), offsets
        if isinstance(offsets.data.data, Reduction):  # type: ignore[attr-defined]
            # Only realize if reduction isn't unrolled
            offsets.realize()

        indices = _pool_offsets_to_indices(
            offsets, kernel_size, x.shape, increments_to_index
        )
        return result, indices

