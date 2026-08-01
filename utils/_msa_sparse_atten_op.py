
def _msa_sparse_atten_op(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    q2k: torch.Tensor,
    cu_seqlens_q: torch.Tensor,
    cu_seqlens_k: torch.Tensor,
    topk: int,
    block_size: int,
    total_k: int,
    max_seqlen_q: int,
    max_seqlen_k: int,
    qheads_per_kv: int,
    scaling: float,
    impl: str,
) -> torch.Tensor:
    """Opaque wrapper around the CuTe-DSL CSR build + block-sparse kernel.

    Registered as a ``torch.library`` custom op so ``torch.compile(fullgraph=True)`` treats the
    whole CSR-build + attention as a single opaque node (no graph break) and ``reduce-overhead``
    CUDA graphs can capture it. The internal ``build_k2q_csr`` output is data-dependent in shape,
    but it never escapes this op (only the fixed-shape ``[total_q, Hq, D]`` attention output does),
    so the fake/meta impl below is exact. The op is functional (no input mutation).
    """
    msa = load_and_register_msa_kernel(impl)
    # CuTe-DSL kernel launches on the ambient ``current_device`` with no internal guard; pin context
    # to the tensors' device so device_map (mixed-GPU) layouts don't reference the wrong context.
    with torch.cuda.device(q.device):
        k2q_row_ptr, k2q_q_indices = msa.build_k2q_csr(
            q2k,
            cu_seqlens_q,
            cu_seqlens_k,
            block_size,
            total_k=total_k,
            max_seqlen_k=max_seqlen_k,
            max_seqlen_q=max_seqlen_q,
            qhead_per_kv=qheads_per_kv,
        )
        attn_output = msa.sparse_atten_func(
            q,
            k,
            v,
            k2q_row_ptr,
            k2q_q_indices,
            topk,
            cu_seqlens_q=cu_seqlens_q,
            cu_seqlens_k=cu_seqlens_k,
            max_seqlen_q=max_seqlen_q,
            max_seqlen_k=max_seqlen_k,
            blk_kv=block_size,
            causal=True,
            softmax_scale=scaling,
        )
    return attn_output.contiguous()

