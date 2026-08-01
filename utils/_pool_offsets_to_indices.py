
def _pool_offsets_to_indices(
    offsets: TensorBox,
    kernel_size: Sequence[int | torch.SymInt],
    input_size: Sequence[int | torch.SymInt],
    increments_to_index: Callable[
        [Sequence[int | torch.SymInt], Sequence[int | torch.SymInt]],
        torch._inductor.virtualized.OpsValue,
    ],
) -> TensorBox:
    n_dim = len(kernel_size)
    offsets_loader = offsets.make_loader()
    window_size = sympy.sympify(functools.reduce(operator.mul, kernel_size))

    def offsets_to_indices(idx):
        offset = offsets_loader(idx)
        offset_sympy = ops.indirect_indexing(offset, window_size)
        reduction_idx = inductor_prims._flattened_index_to_nd(offset_sympy, kernel_size)
        idhw = increments_to_index(idx, reduction_idx)
        return ops.index_expr(
            inductor_prims._flatten_index(idhw, input_size[-n_dim:]), torch.int64
        )

    indices = Pointwise.create(
        device=offsets.get_device(),
        dtype=torch.int64,
        inner_fn=offsets_to_indices,
        ranges=offsets.get_size(),
    )
    return indices

