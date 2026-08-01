
def make_flex_block_causal_mask(
    attention_mask_2d: torch.Tensor,
    attention_chunk_size: int | None = None,
    query_length=None,
    key_length=None,
    offsets: tuple[Offset, Offset] | None = None,
    is_causal: bool | None = True,
) -> "BlockMask":
    """
    IMPORTANT NOTICE: This function is deprecated in favor of using the mask primitives in `masking_utils.py`,
    and will be removed in a future version without warnings. New code should not use it. It is only kept here
    for BC for now, while models using it are being patched accordingly.

    Create a block (causal) document mask for a batch of sequences, both packed and unpacked.
    Create Block (causal) logic and passing it into :func:`torch.nn.attention.flex_attention.create_block_mask`.
    The resultant BlockMask is a compressed representation of the full (causal) block
    mask. BlockMask is essential for performant computation of flex attention.
    See: https://pytorch.org/blog/flexattention/

    Args:
        attention_mask_2d (torch.Tensor): Attention mask for packed and padded sequences
        of shape (batch_size, total_seq_len). e.g.

        For unpacked sequence:
        [[1, 1, 1, 1, 0, 0, 0],
         [1, 1, 1, 1, 1, 0, 0]]

        For packed sequence:
        [[1, 1, 1, 2, 2, 2, 0],
         [1, 1, 2, 2, 2, 3, 3]]

    Returns:
        BlockMask
    """
    batch_size, total_seq_len = attention_mask_2d.shape
    if not key_length:
        key_length = total_seq_len
    if not query_length:
        query_length = total_seq_len
    # older torch (2.5.x) cannot handle sequences not in multiples of 128 (default block size)
    pad_len = ((key_length // flex_default_block_size) + 1) * flex_default_block_size
    attention_mask_2d = torch.nn.functional.pad(attention_mask_2d, value=0, pad=(0, pad_len - key_length))
    device = attention_mask_2d.device
    document_ids = attention_mask_2d.clone()

    if attention_chunk_size is not None:
        # we create an arange, then we just // by chunk size to get [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]
        chunk_idxs = (document_ids.clone().fill_(1).cumsum(-1) - 1) // (attention_chunk_size)

    # Instead of passing a tensor mask, flex attention requires a mask_mod function
    # that determines which elements of QK^T should be included in the attention
    # computation prior to the softmax. For sample packing, we need both the
    # logic for both causal mask and document mask. See PyTorch's official
    # blog post for more details: https://pytorch.org/blog/flexattention/#mask-mods
    def causal_mask_mod(batch_idx, head_idx, q_idx, kv_idx):
        """
        Defines the logic of a block causal mask by combining both a standard causal mask
        and a block diagonal document mask.
        See :func:`~torchtune.modules.attention_utils.create_block_causal_mask`
        for an illustration.
        """
        causal_mask = q_idx >= kv_idx  # not valid when decoding
        document_mask = document_ids[batch_idx, q_idx] == document_ids[batch_idx, kv_idx]
        padding_mask = attention_mask_2d[batch_idx, q_idx] > 0
        final_mask = causal_mask & padding_mask & document_mask
        return final_mask

    def chunk_causal_mask_mod(batch_idx, head_idx, q_idx, kv_idx):
        """
        Combines the chunk mask with the causal mask for chunked attention.
        """
        chunk_mask = chunk_idxs[batch_idx, q_idx] == chunk_idxs[batch_idx, kv_idx]
        causal_doc_mask = causal_mask_mod(batch_idx, head_idx, q_idx, kv_idx)
        return chunk_mask & causal_doc_mask

    def default_mask_mod(batch_idx, head_idx, q_idx, kv_idx):
        """
        Utilizes default attention mask to enable encoder and encoder-decoder
        attention masks.
        """
        document_mask = document_ids[batch_idx, q_idx] == document_ids[batch_idx, kv_idx]
        # kv indexing is crucial in order to work correctly
        padding_mask = attention_mask_2d[batch_idx, kv_idx] > 0
        final_mask = padding_mask & document_mask
        return final_mask

    if not is_causal:
        mask_mod_maybe_combined = default_mask_mod
    else:
        mask_mod_maybe_combined = causal_mask_mod if attention_chunk_size is None else chunk_causal_mask_mod

    if offsets is not None:
        q_offset = offsets[0].to(device)
        kv_offset = offsets[1].to(device)

        def mask_mod(batch_idx, head_idx, q_idx, kv_idx):
            offset_q = q_idx + q_offset
            offset_kv = kv_idx + kv_offset
            return mask_mod_maybe_combined(batch_idx, head_idx, offset_q, offset_kv)
    else:
        mask_mod = mask_mod_maybe_combined

    return create_block_mask(
        mask_mod=mask_mod,
        B=batch_size,
        H=None,  # attention head
        Q_LEN=query_length,
        KV_LEN=key_length,
        device=device,
        # compiling the mask is not BC with older torch
        _compile=not is_torch_less_or_equal("2.5.1"),
    )

