
def register_jagged_ops():
    # Avoid circular import by importing here
    from .lowering import fallback_handler, is_integer_type, register_lowering

    # pyre-ignore[56]
    @register_lowering(torch.ops.aten._jagged_to_padded_dense_forward.default)
    def _jagged_to_padded_dense_forward(
        jagged_values: TensorBox,
        jagged_offsets: list[TensorBox],
        max_lengths: list[int],  # list of ints/SymInts
        padding_value: float = 0.0,
    ) -> TensorBox:
        device = jagged_values.get_device_or_error()
        dtype = jagged_values.get_dtype()

        jagged_values_size = jagged_values.get_size()

        # only handle the common case of a single jagged dimension
        if (
            len(jagged_offsets) != 1
            or device.type != "cuda"
            or device != jagged_offsets[0].get_device()
            or len(jagged_values_size) != 2
            or len(jagged_offsets[0].get_size()) != 1
            or len(max_lengths) != len(jagged_offsets)
            or not is_integer_type(jagged_offsets[0])
        ):
            return fallback_handler(
                torch.ops.aten._jagged_to_padded_dense_forward.default,
                add_to_fallback_set=False,
            )(
                jagged_values,
                jagged_offsets,
                max_lengths,
                padding_value,
            )

        offsets: TensorBox = jagged_offsets[0]  # type: ignore[assignment]
        offsets_len = offsets.get_size()[0]
        offsets_dtype = offsets.get_dtype()
        batch_size = offsets_len - 1
        max_seq_len = max_lengths[0]
        embedding_len = jagged_values_size[1]
        jagged_len = jagged_values_size[0]

        output_size = [batch_size, max_seq_len, embedding_len]

        values_loader = jagged_values.make_loader()
        offsets_loader = offsets.make_loader()

        # pyre-ignore[2,3,53]
        def inner_fn(index):
            # dense tensor size: [B, N, D]
            batch_idx, seq_idx, emb_idx = index
            jagged_idx, end_idx = dense_idx_to_jagged_idx(
                batch_idx=batch_idx,
                seq_idx=seq_idx,
                offsets_loader=offsets_loader,
                jagged_len=jagged_len,
            )
            return ops.masked(
                ops.lt(
                    ops.index_expr(jagged_idx, offsets_dtype),
                    end_idx,
                ),
                lambda: values_loader([jagged_idx, emb_idx]),
                padding_value,
            )

        return Pointwise.create(
            device=device,
            dtype=dtype,
            inner_fn=inner_fn,
            ranges=output_size,
        )

    def _dense_to_jagged_forward_impl(
        fallback_op,  # pyre-ignore[2]
        dense: TensorBox,
        jagged_offsets: list[TensorBox],
        jagged_len: int | None = None,
    ) -> TensorBox:
        device = dense.get_device_or_error()
        dtype = dense.get_dtype()

        dense_size = dense.get_size()

        # only handle the common case of a single jagged dimension
        if (
            len(jagged_offsets) != 1
            or device.type != "cuda"
            or device != jagged_offsets[0].get_device()
            or len(jagged_offsets[0].get_size()) != 1
            or len(dense_size) != 3
            or jagged_len is None
            or not is_integer_type(jagged_offsets[0])
        ):
            return fallback_handler(fallback_op, add_to_fallback_set=False)(
                dense,
                jagged_offsets,
                jagged_len,
            )

        offsets: TensorBox = jagged_offsets[0]  # type: ignore[assignment]
        offsets_dtype = offsets.get_dtype()
        batch_size = dense_size[0]
        max_seq_len = dense_size[1]
        embedding_len = dense_size[-1]

        output_size = [jagged_len, embedding_len]

        dense_loader = dense.make_loader()
        offsets_loader = offsets.make_loader()

        inverse_offsets = get_inverse_offsets(
            offsets=offsets,
            jagged_len=jagged_len,
        )
        inverse_offsets_loader = inverse_offsets.make_loader()

        # pyre-ignore[2,3,53]
        def inner_fn(index):
            # jagged tensor size: [sum_B(N_B), D]
            jagged_idx, emb_idx = index
            batch_idx, seq_idx = jagged_idx_to_dense_idx(
                jagged_idx=jagged_idx,
                offsets_loader=offsets_loader,
                inverse_offsets_loader=inverse_offsets_loader,
                batch_size=batch_size,
                max_seq_len=max_seq_len,
                offsets_dtype=offsets_dtype,
            )
            return ops.masked(
                ops.lt(
                    ops.index_expr(seq_idx, offsets_dtype),
                    ops.index_expr(max_seq_len, offsets_dtype),
                ),
                lambda: dense_loader([batch_idx, seq_idx, emb_idx]),
                0.0,  # jagged sequence longer than max_seq_len
            )

        return Pointwise.create(
            device=device,
            dtype=dtype,
            inner_fn=inner_fn,
            ranges=output_size,
        )

    # pyre-ignore[56]
    @register_lowering(torch.ops.aten._padded_dense_to_jagged_forward)
    def _dense_to_jagged_forward(
        dense: TensorBox,
        jagged_offsets: list[TensorBox],
        jagged_len: int | None = None,
    ) -> TensorBox:
        return _dense_to_jagged_forward_impl(
            fallback_op=torch.ops.aten._padded_dense_to_jagged_forward.default,
            dense=dense,
            jagged_offsets=jagged_offsets,
            jagged_len=jagged_len,
        )

