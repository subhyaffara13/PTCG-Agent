
def _validate_msa_init(module, query: torch.Tensor, dropout: float) -> None:
    """Validate kernel capability, dropout and configured topk once per attention module.

    Mirrors the flash-attention integration, which checks capability/dropout at model init rather
    than on every forward. The check is cached on the module so the hot path never re-runs it.

    There is no SDPA fallback: a sparse layer either runs the MSA kernel or this raises. Serves both
    prefill (q_len > 1) and single-token decode (q_len == 1) -- decode is just a varlen call with one
    query slot, so there is no context-length threshold.
    """
    if query.device.type != "cuda" or torch.cuda.get_device_capability(query.device)[0] != 10:
        raise RuntimeError(
            "MSA block-sparse attention requires an SM100 / Blackwell CUDA device. "
            "Select a different `attn_implementation` on unsupported hardware."
        )
    if query.shape[-1] != MSA_SUPPORTED_HEAD_DIM:
        raise ValueError(f"MSA block-sparse attention only supports head_dim {MSA_SUPPORTED_HEAD_DIM}.")
    if module.indexer.block_size != MSA_SUPPORTED_BLOCK_SIZE:
        raise ValueError(f"MSA block-sparse attention only supports block_size {MSA_SUPPORTED_BLOCK_SIZE}.")
    if dropout != 0.0:
        raise ValueError("MSA block-sparse attention does not support attention dropout; set `attention_dropout=0`.")
    topk = module.indexer.topk_blocks
    if topk not in MSA_SUPPORTED_TOPK:
        raise ValueError(
            f"MSA block-sparse attention only supports topk in {MSA_SUPPORTED_TOPK}, got `{topk}`. "
            "Set `index_topk_blocks` to a supported value."
        )

