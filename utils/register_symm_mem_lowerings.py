
def register_symm_mem_lowerings():
    """
    Register lowerings for symmetric memory (symm_mem) operations.
    """
    try:
        symm_mem = torch.ops.symm_mem
        # Check for an actual operation, not just the namespace.
        # torch.ops.symm_mem is a lazy namespace that always exists,
        # but the operations may not exist on non-CUDA platforms or
        # when USE_DISTRIBUTED is disabled.
        symm_mem.one_shot_all_reduce
    except AttributeError:
        log.info("symm_mem ops not available, skipping symm_mem lowerings")
        return

    from torch._library._out_variant import register_out_variant

    # Register manual out variant mappings for symm_mem ops.
    register_out_variant(
        symm_mem.one_shot_all_reduce.default,
        symm_mem.one_shot_all_reduce_out.default,
    )
    register_out_variant(
        symm_mem.one_shot_all_reduce_copy.default,
        symm_mem.one_shot_all_reduce_copy_out.default,
    )

    from .lowering import register_lowering

    def _copy_input_to_comm_buffer(
        inp: ir.TensorBox,
        comm_buffer_type: ir.CommBufferType,
        group_name: "torch.distributed.distributed_c10d.GroupName",
    ) -> ir.TensorBox:
        """
        Fallback: insert a Pointwise identity copy allocated in P2P via
        CommBufferLayout.  Used when we don't control the input's allocation.
        """
        inp.realize()
        copy = ir.Pointwise.create(
            device=inp.get_device(),
            dtype=inp.get_dtype(),
            inner_fn=inp.make_loader(),
            ranges=inp.get_size(),
        )
        realize_as_comm_buffer(copy, comm_buffer_type, group_name)
        return copy

    def _maybe_realize_symm_mem(
        inp: ir.TensorBox,
        group_name: str,  # type: ignore[arg-type]
    ) -> ir.TensorBox:
        """
        Ensure inp is in P2P memory for a symm_mem collective.

        If inductor controls the buffer's allocation (ComputedBuffer,
        or any buffer with FlexibleLayout/FixedLayout), switch its
        layout to CommBufferLayout in-place, zero-copy.

        If inductor does not control allocation (e.g. InputBuffer),
        insert a Pointwise identity copy into a new CommBufferLayout buffer.
        This adds an extra Triton kernel. Returns the possibly new TensorBox.

        TODO(tianrengao): eliminate the extra kernel for static-shape
        InputBuffers by pre-allocating P2P memory in the wrapper and DMA .copy_()
        """
        if can_realize_as_comm_buffer(inp, ir.CommBufferType.SYMM_MEM):
            realize_as_comm_buffer(inp, ir.CommBufferType.SYMM_MEM, group_name)  # type: ignore[arg-type]
            return inp
        else:
            return _copy_input_to_comm_buffer(
                inp,
                ir.CommBufferType.SYMM_MEM,
                group_name,  # type: ignore[arg-type]
            )

    @register_lowering(symm_mem.one_shot_all_reduce)
    def _symm_mem_one_shot_all_reduce(
        inp: ir.TensorBox,
        reduce_op: str,
        group_name: str,
    ):
        inp = _maybe_realize_symm_mem(inp, group_name)
        return pytree.tree_map(
            ir.TensorBox.create,
            ir.FallbackKernel.create(
                symm_mem.one_shot_all_reduce.default,
                inp,
                reduce_op,
                group_name,
            ),
        )

    @register_lowering(symm_mem.one_shot_all_reduce_out)
    def _symm_mem_one_shot_all_reduce_out(
        inp: ir.TensorBox,
        reduce_op: str,
        group_name: str,
        out: ir.TensorBox,
    ):
        inp = _maybe_realize_symm_mem(inp, group_name)
        return pytree.tree_map(
            ir.TensorBox.create,
            ir.FallbackKernel.create(
                symm_mem.one_shot_all_reduce_out.default,
                inp,
                reduce_op,
                group_name,
                out,
            ),
        )

    @register_lowering(symm_mem.one_shot_all_reduce_copy)
    def _symm_mem_one_shot_all_reduce_copy(
        symm_buffer: ir.TensorBox,
        local_input: ir.TensorBox,
        reduce_op: str,
        group_name: str,
    ):
        symm_buffer = _maybe_realize_symm_mem(symm_buffer, group_name)
        return pytree.tree_map(
            ir.TensorBox.create,
            ir.FallbackKernel.create(
                symm_mem.one_shot_all_reduce_copy.default,
                symm_buffer,
                local_input,
                reduce_op,
                group_name,
            ),
        )

    @register_lowering(symm_mem.one_shot_all_reduce_copy_out)
    def _symm_mem_one_shot_all_reduce_copy_out(
        symm_buffer: ir.TensorBox,
        local_input: ir.TensorBox,
        reduce_op: str,
        group_name: str,
        out: ir.TensorBox,
    ):
        symm_buffer = _maybe_realize_symm_mem(symm_buffer, group_name)
        return pytree.tree_map(
            ir.TensorBox.create,
            ir.FallbackKernel.create(
                symm_mem.one_shot_all_reduce_copy_out.default,
                symm_buffer,
                local_input,
                reduce_op,
                group_name,
                out,
            ),
        )

    @register_lowering(symm_mem.two_shot_all_reduce_)
    def _symm_mem_two_shot_all_reduce_(
        inp: ir.TensorBox,
        reduce_op: str,
        group_name: str,
    ):
        inp = _maybe_realize_symm_mem(inp, group_name)
        ir.FallbackKernel.create(
            symm_mem.two_shot_all_reduce_.default,
            inp,
            reduce_op,
            group_name,
        )
        return inp

    @register_lowering(symm_mem.two_shot_all_reduce_out)
    def _symm_mem_two_shot_all_reduce_out(
        inp: ir.TensorBox,
        reduce_op: str,
        group_name: str,
        output: ir.TensorBox,
    ):
        inp = _maybe_realize_symm_mem(inp, group_name)
        return pytree.tree_map(
            ir.TensorBox.create,
            ir.FallbackKernel.create(
                symm_mem.two_shot_all_reduce_out.default,
                inp,
                reduce_op,
                group_name,
                output,
            ),
        )

    @register_lowering(symm_mem.multimem_all_reduce_)
    def _symm_mem_multimem_all_reduce_(
        inp: ir.TensorBox,
        reduce_op: str,
        group_name: str,
    ):
        inp = _maybe_realize_symm_mem(inp, group_name)
        ir.FallbackKernel.create(
            symm_mem.multimem_all_reduce_.default,
            inp,
            reduce_op,
            group_name,
        )
        return inp

    @register_lowering(symm_mem.multimem_one_shot_all_reduce)
    def _symm_mem_multimem_one_shot_all_reduce(
        inp: ir.TensorBox,
        reduce_op: str,
        group_name: str,
    ):
        inp = _maybe_realize_symm_mem(inp, group_name)
        return pytree.tree_map(
            ir.TensorBox.create,
            ir.FallbackKernel.create(
                symm_mem.multimem_one_shot_all_reduce.default,
                inp,
                reduce_op,
                group_name,
            ),
        )

    @register_lowering(symm_mem.multimem_one_shot_all_reduce_out)
    def _symm_mem_multimem_one_shot_all_reduce_out(
        inp: ir.TensorBox,
        reduce_op: str,
        group_name: str,
        out: ir.TensorBox,
    ):
        inp = _maybe_realize_symm_mem(inp, group_name)
        return pytree.tree_map(
            ir.TensorBox.create,
            ir.FallbackKernel.create(
                symm_mem.multimem_one_shot_all_reduce_out.default,
                inp,
                reduce_op,
                group_name,
                out,
            ),
        )

    @register_lowering(symm_mem.multimem_one_shot_reduce_out)
    def _symm_mem_multimem_one_shot_reduce_out(
        inp: ir.TensorBox,
        reduce_op: str,
        root: int,
        group_name: str,
        out: ir.TensorBox,
    ):
        inp = _maybe_realize_symm_mem(inp, group_name)
        return pytree.tree_map(
            ir.TensorBox.create,
            ir.FallbackKernel.create(
                symm_mem.multimem_one_shot_reduce_out.default,
                inp,
                reduce_op,
                root,
                group_name,
                out,
            ),
        )

    @register_lowering(symm_mem.multimem_all_gather_out)
    def _symm_mem_multimem_all_gather_out(
        inp: ir.TensorBox,
        group_name: str,
        out: ir.TensorBox,
    ):
        inp = _maybe_realize_symm_mem(inp, group_name)
        return pytree.tree_map(
            ir.TensorBox.create,
            ir.FallbackKernel.create(
                symm_mem.multimem_all_gather_out.default,
                inp,
                group_name,
                out,
            ),
        )

    @register_lowering(symm_mem.reduce_scatter_out)
    def _symm_mem_reduce_scatter_out(
        inp: ir.TensorBox,
        group_name: str,
        split_last_dim: bool,
        output: ir.TensorBox,
    ):
        inp = _maybe_realize_symm_mem(inp, group_name)
        return pytree.tree_map(
            ir.TensorBox.create,
            ir.FallbackKernel.create(
                symm_mem.reduce_scatter_out.default,
                inp,
                group_name,
                split_last_dim,
                output,
            ),
        )

    @register_lowering(symm_mem.all_to_all_vdev)
    def _symm_mem_all_to_all_vdev(
        inp: ir.TensorBox,
        out: ir.TensorBox,
        in_splits: ir.TensorBox,
        out_splits_offsets: ir.TensorBox,
        group_name: str,
    ):
        inp = _maybe_realize_symm_mem(inp, group_name)
        out = _maybe_realize_symm_mem(out, group_name)
        ir.FallbackKernel.create(
            symm_mem.all_to_all_vdev.default,
            inp,
            out,
            in_splits,
            out_splits_offsets,
            group_name,
        )
        return None

    @register_lowering(symm_mem.all_to_all_vdev_2d)
    def _symm_mem_all_to_all_vdev_2d(
        inp: ir.TensorBox,
        out: ir.TensorBox,
        in_splits: ir.TensorBox,
        out_splits_offsets: ir.TensorBox,
        group_name: str,
        major_align=None,
    ):
        inp = _maybe_realize_symm_mem(inp, group_name)
        out = _maybe_realize_symm_mem(out, group_name)
        ir.FallbackKernel.create(
            symm_mem.all_to_all_vdev_2d.default,
            inp,
            out,
            in_splits,
            out_splits_offsets,
            group_name,
            major_align,
        )
        return None

    @register_lowering(symm_mem.all_to_all_vdev_2d_offset)
    def _symm_mem_all_to_all_vdev_2d_offset(
        inp: ir.TensorBox,
        out: ir.TensorBox,
        in_splits_offsets: ir.TensorBox,
        out_splits_offsets: ir.TensorBox,
        group_name: str,
    ):
        inp = _maybe_realize_symm_mem(inp, group_name)
        out = _maybe_realize_symm_mem(out, group_name)
        ir.FallbackKernel.create(
            symm_mem.all_to_all_vdev_2d_offset.default,
            inp,
            out,
            in_splits_offsets,
            out_splits_offsets,
            group_name,
        )
        return None

    @register_lowering(symm_mem.tile_reduce)
    def _symm_mem_tile_reduce(
        in_tile: ir.TensorBox,
        out_tile: ir.TensorBox,
        root: int,
        group_name: str,
        reduce_op: str = "sum",
    ):
        in_tile = _maybe_realize_symm_mem(in_tile, group_name)
        out_tile = _maybe_realize_symm_mem(out_tile, group_name)
        ir.FallbackKernel.create(
            symm_mem.tile_reduce.default,
            in_tile,
            out_tile,
            root,
            group_name,
            reduce_op,
        )
        return None

    @register_lowering(symm_mem.multi_root_tile_reduce)
    def _symm_mem_multi_root_tile_reduce(
        in_tiles,  # list of TensorBox
        out_tile: ir.TensorBox,
        roots,  # list of int
        group_name: str,
        reduce_op: str = "sum",
    ):
        for i, in_tile in enumerate(in_tiles):
            in_tiles[i] = _maybe_realize_symm_mem(in_tile, group_name)
        out_tile = _maybe_realize_symm_mem(out_tile, group_name)
        ir.FallbackKernel.create(
            symm_mem.multi_root_tile_reduce.default,
            in_tiles,
            out_tile,
            roots,
            group_name,
            reduce_op,
        )
        return None

