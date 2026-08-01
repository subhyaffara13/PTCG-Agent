
def _create_cp_block_mask(
    mask_mod: _mask_mod_signature,
    B: int,
    H: int,
    Q_LEN: int,
    KV_LEN: int,
    device_mesh: DeviceMesh,
    load_balancer: _LoadBalancer | None = None,
) -> BlockMask:
    """
    Creates a specialized BlockMask for Context Parallel FlexAttention.

    This function creates a BlockMask that enables computation of attention results
    for sharded Q attending to global KV. The mask appropriately handles the query
    index offset required when each rank operates on a shard of the query sequence
    while accessing the full key-value sequence.

    The function internally rewrites the provided mask_mod function to translate local
    query indices to global query indices, ensuring that the masking logic is applied
    correctly across the distributed computation.

    Args:
        mask_mod (Callable): Mask function that operates on global attention indices.
        B (int): Batch size.
        H (int): Number of query heads.
        Q_LEN (int): Global sequence length of the query.
        KV_LEN (int): Global sequence length of the key/value.
        device_mesh (DeviceMesh): Device mesh used for context parallelism.
        load_balancer (Optional[:class:`_LoadBalancer`]): The load-balancer used to rearrange
            QKV before sharding. This will be used to modify the block_mask generated.

    Returns:
        BlockMask: A block mask configured for the local query shard that can be used
            with flex_attention() for the given cp_mesh.

    Raises:
        NotImplementedError: If Q_LEN is not divisible by (CP world size * BLOCK_SIZE).

    Warning:
        Currently requires Q_LEN to be divisible by CP mesh world size * BLOCK_SIZE
        (BLOCK_SIZE defaults to 128). This constraint exists because the BlockMask
        must handle both padding and offsets correctly. For example, if Q_LEN is 384,
        CP world size is 2, and BLOCK_SIZE is 128, the local Q_LEN would be 192. In
        such cases, both rank0 and rank1 would have paddings in their local BlockMasks.
        Support for padding in this scenario is planned for future work.

    """

    from torch.nn.attention.flex_attention import _DEFAULT_SPARSE_BLOCK_SIZE

    if Q_LEN % (device_mesh.size() * _DEFAULT_SPARSE_BLOCK_SIZE) != 0:
        raise NotImplementedError(
            f"Q_LEN {Q_LEN} is not divisible by CP mesh world size {device_mesh.size()} * "
            f"BLOCK_SIZE {_DEFAULT_SPARSE_BLOCK_SIZE}. This is not supported yet. "
        )

    global _compiled_create_block_mask
    if _compiled_create_block_mask is None:
        _compiled_create_block_mask = torch.compile(
            create_block_mask, dynamic=False, fullgraph=True
        )
    compiled_create_block_mask = _compiled_create_block_mask

    def _rewrite_mask_mod(
        mask_mod: _mask_mod_signature,
        rank: int,
        block_size: int,
        local_q_size: int,
        qkv_rearrange_indices: torch.Tensor | None = None,
    ) -> _mask_mod_signature:
        if not (qkv_rearrange_indices is None or qkv_rearrange_indices.ndim == 2):
            raise AssertionError(
                "load balance index expects shape (1, seq_len) or (B, seq_len) "
                f"but got {qkv_rearrange_indices.shape}."
            )

        def qkv_idx_restore(
            b: torch.Tensor, idx_post_rearrange: torch.Tensor
        ) -> torch.Tensor:
            if qkv_rearrange_indices is not None:
                if (
                    qkv_rearrange_indices.size(0) == 1
                ):  # identical load-balance in batch
                    idx_pre_rearrange = qkv_rearrange_indices[0][idx_post_rearrange]
                else:
                    idx_pre_rearrange = qkv_rearrange_indices[b][idx_post_rearrange]
            else:
                idx_pre_rearrange = idx_post_rearrange

            return idx_pre_rearrange

        def local_q_idx_to_q_idx(local_q_idx: torch.Tensor) -> torch.Tensor:
            # calculate local block_idx and block_offset
            local_blk_idx, local_blk_offset = (
                local_q_idx // block_size,
                local_q_idx % block_size,
            )
            # NOTE: load balancing is not used
            local_num_blocks = local_q_size // block_size
            blk_idx = local_num_blocks * rank + local_blk_idx
            return blk_idx * block_size + local_blk_offset

        return lambda b, h, q_idx, kv_idx: mask_mod(
            b,
            h,
            qkv_idx_restore(b, local_q_idx_to_q_idx(q_idx)),
            qkv_idx_restore(b, kv_idx),
        )

    cp_rank = device_mesh.get_local_rank()
    cp_group_size = device_mesh.size()
    load_balancer = load_balancer or _create_default_load_balancer(
        Q_LEN, cp_group_size, device_mesh.device_type
    )
    Q_SHARD_LEN = Q_LEN // cp_group_size
    block_size = _DEFAULT_SPARSE_BLOCK_SIZE

    rearrange_indices = (
        load_balancer._generate_indices(restore=False) if load_balancer else None
    )
    block_mask = compiled_create_block_mask(
        _rewrite_mask_mod(
            mask_mod,
            cp_rank,
            block_size,
            Q_SHARD_LEN,
            qkv_rearrange_indices=rearrange_indices,
        ),
        B,
        H,
        Q_SHARD_LEN,
        KV_LEN,
        device=device_mesh.device_type,
        BLOCK_SIZE=(block_size, block_size),
    )
    return block_mask

