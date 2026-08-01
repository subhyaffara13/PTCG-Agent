
def rotary_embedding(
    X: torch.Tensor,
    cos_cache: torch.Tensor,
    sin_cache: torch.Tensor,
    position_ids: torch.Tensor | None = None,
    *,
    interleaved: bool = False,
    num_heads: int = 0,
    rotary_embedding_dim: int = 0,
) -> torch.Tensor:
    """RotaryEmbedding op in ONNX.

    https://onnx.ai/onnx/operators/onnx__RotaryEmbedding.html

    RotaryEmbedding is the implementation of rotary positional embeddings (RoPE) based on the paper https://arxiv.org/pdf/2104.09864.
    The key advantage of RoPE is that it allows the model to understand both the absolute position of a token and the relative distances
    between tokens. This is achieved through a rotational mechanism where the extent of rotation is computed based on the token's absolute position (position_ids).

    The rotational mechanism is defined by sine and cosine functions that are used to represent the rotation angles.
    For each token in the sequence, its positional embedding is computed by rotating its embedding vector. This is done by splitting the
    embedding vector either into two halves or interleaving every alternate token and applying the rotation matrix to each half of the embedding vector.
    The rotation matrix is parameterized by the token's position in the sequence. The rotated halves of the embedding vector are concatenated
    to form the final positional embedding for each token. The rotated positional embeddings are used in the self-attention mechanism.
    The rotation ensures that the model captures both absolute and relative positional information.

    Args:
        X: The input tensor representing the token embeddings. 4D tensor with
            shape `(batch_size, num_heads, sequence_length, head_size)` or 3D tensor
            with shape `(batch_size, sequence_length, hidden_size)`. For cases with
            a 4D input tensor, `head_size` has to be even. For cases with a 3D input
            tensor, `num_heads` attribute must be provided and `hidden_size` must
            be an even multiple of `num_heads` where `hidden_size = num_heads * head_size`
        cos_cache: The cosine values for the rotation. 2D tensor with shape `(max_position_id_plus_1, head_size / 2)`
            for full rotation or `(max_position_id_plus_1, rotary_embedding_dim / 2)`
            for partial rotation when `position_ids` are provided. 3D tensor with shape
            `(batch_size, sequence_length, head_size / 2)` for full rotation or
            `(batch_size, sequence_length, rotary_embedding_dim / 2)` for partial
            rotation when `position_ids` are not provided. `max_position_id_plus_1`
            is a parameter to the model.
        sin_cache: The sine values for the rotation. 2D tensor with shape `(max_position_id_plus_1, head_size / 2)`
            for full rotation or `(max_position_id_plus_1, rotary_embedding_dim / 2)`
            for partial rotation when `position_ids` are provided. 3D tensor with shape
            `(batch_size, sequence_length, head_size / 2)` for full rotation or
            `(batch_size, sequence_length, rotary_embedding_dim / 2)` for partial rotation
            when `position_ids` are not provided. `max_position_id_plus_1` is a parameter
            to the model.
        position_ids: The position indices for the tokens. 2D tensor with shape
            `(batch_size, sequence_length)`.
        interleaved: Rotate using interleaved pattern. Default value is 0 (False).
        num_heads: Number of attention heads. Must be provided when input is a 3D tensor.
        rotary_embedding_dim: Rotary embedding dimension used to apply partial rotary embeddings.

    Returns:
        Tensor with same shape as input.
    """
    return _impl.rotary_embedding_23(
        X,
        cos_cache,
        sin_cache,
        position_ids=position_ids,
        interleaved=interleaved,
        num_heads=num_heads,
        rotary_embedding_dim=rotary_embedding_dim,
    )

