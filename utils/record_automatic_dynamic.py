
def record_automatic_dynamic(
    tx: "InstructionTranslatorBase", name: str, e: torch.Tensor
) -> FrameStateSizeEntry:
    # This mimics stride inference algorithm in _create_symbolic_sizes_strides_storage_offset
    ex_size = e.size()
    if not is_sparse_any(e):
        ex_stride = e.stride()
        dim = e.dim()

        stride = [None] * dim
        pending = [(ex_stride[i], -i) for i in range(dim)]
        pending.sort(key=_nested_int_aware_sort)
        candidates = {}
        for i_stride, neg_i in pending:
            i = -neg_i
            # pyrefly: ignore [unsupported-operation]
            stride[i] = candidates.get(i_stride, i_stride)
            # pyrefly: ignore [no-matching-overload]
            candidates.setdefault(i_stride * ex_size[i], InferStride(i))
    else:
        # pyrefly: ignore [implicit-any]
        stride = []

    return process_automatic_dynamic(
        # type: ignore[arg-type]ks
        tx,
        name,
        # type: ignore[arg-type]
        FrameStateSizeEntry.make_tensor(tuple(ex_size), tuple(stride)),
    )

