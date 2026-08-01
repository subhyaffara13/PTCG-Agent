
def _sparse_attention(module, query, key, value, scaling, block_indices, block_size, cache_position):
    bsz, num_q_heads, q_len, head_dim = query.shape
    num_kv_heads, k_len = key.shape[1], key.shape[2]
    qheads_per_kv = num_q_heads // num_kv_heads
    topk = block_indices.shape[-1]

    # The indexer emits `min(index_topk_blocks, num_key_blocks)` selected blocks, so on sequences with
    # fewer key blocks than the configured budget the width lands on an arbitrary value (e.g. 12) that the
    # `SparseK2qCsrBuilderSm100` CSR builder rejects -- it only accepts a CSR width in `MSA_SUPPORTED_TOPK`.
    # Right-pad the selection up to the next supported width with `-1`, the same empty-slot sentinel the
    # kernel already skips, so behaviour is unchanged and the width is always one the builder accepts. The
    # width is a Python int (static under `torch.compile`), so this stays fullgraph / cudagraph stable.
    padded_topk = next(t for t in MSA_SUPPORTED_TOPK if t >= topk)
    if padded_topk != topk:
        pad = block_indices.new_full((*block_indices.shape[:-1], padded_topk - topk), -1)
        block_indices = torch.cat([block_indices, pad], dim=-1)
        topk = padded_topk

    # Flatten the batch dim into a packed varlen layout [total, H, head_dim] + cu_seqlens. The
    # query boundary is a fixed stride (every row is `q_len` long), built device-side with no host
    # sync so it stays compile/cudagraph stable.
    q = query.transpose(1, 2).reshape(bsz * q_len, num_q_heads, head_dim).contiguous()
    k = key.transpose(1, 2).reshape(bsz * k_len, num_kv_heads, head_dim).contiguous()
    v = value.transpose(1, 2).reshape(bsz * k_len, num_kv_heads, head_dim).contiguous()
    cu_seqlens_q = torch.arange(0, (bsz + 1) * q_len, q_len, device=q.device, dtype=torch.int32)
    # Under a StaticCache `k_len` is the pre-allocated buffer (`max_cache_len`), not the valid length,
    # so a packed `[0, k_len, 2*k_len, ...]` boundary would let the kernel's causal attend zero-padded
    # future slots. For bsz==1 the real boundary is `[0, valid_k]` (valid_k = cache_position[-1]+1) built
    # as a device tensor (no host sync) -- `build_k2q_csr` reads only the host shape hints `total_k`/
    # `max_seqlen_k` (kept fixed at `bsz*k_len`/`k_len` below), so this stays compile/cudagraph stable.
    if bsz == 1 and cache_position is not None:
        valid_k = (cache_position[-1] + 1).to(torch.int32).reshape(1)
        cu_seqlens_k = torch.cat([torch.zeros(1, device=q.device, dtype=torch.int32), valid_k])
    else:
        cu_seqlens_k = torch.arange(0, (bsz + 1) * k_len, k_len, device=q.device, dtype=torch.int32)

    q2k = block_indices.to(torch.int32)
    q2k = q2k.reshape(bsz * q_len, topk).unsqueeze(0).expand(num_kv_heads, -1, -1).contiguous()

    # Opaque custom op: keeps the CuTe-DSL CSR build + block-sparse kernel as a single graph node
    # so ``torch.compile(fullgraph=True)`` doesn't break and ``reduce-overhead`` CUDA graphs capture it.
    attn_output = _msa_sparse_atten_op(
        q,
        k,
        v,
        q2k,
        cu_seqlens_q,
        cu_seqlens_k,
        topk,
        block_size,
        bsz * k_len,
        q_len,
        k_len,
        qheads_per_kv,
        scaling,
        module.config._attn_implementation,
    )
    return attn_output.reshape(bsz, q_len, num_q_heads, head_dim)

