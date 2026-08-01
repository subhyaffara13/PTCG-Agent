
def attention(
    Q: torch.Tensor,
    K: torch.Tensor,
    V: torch.Tensor,
    attn_mask: torch.Tensor | None = None,
    past_key: torch.Tensor | None = None,
    past_value: torch.Tensor | None = None,
    *,
    is_causal: bool = False,
    kv_num_heads: int = 0,
    q_num_heads: int = 0,
    qk_matmul_output_mode: int = 0,
    scale: float | None = None,
    softcap: float = 0.0,
    softmax_precision: int | None = None,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """Attention op in ONNX.

    https://onnx.ai/onnx/operators/onnx__Attention.html

    Computes scaled dot product attention on query, key and value tensors, using an optional attention mask if passed.

    This operator covers self and cross variants of the attention operation based on sequence lengths of K, Q and V.

    For self attention, ``kv_sequence_length`` equals to ``q_sequence_length``.

    For cross attention, query and key might have different lengths.

    This operator also covers the 3 following variants based on the number of heads:

    1. Multi-headed Attention (MHA): Described in the paper https://arxiv.org/pdf/1706.03762, `q_num_heads = kv_num_heads`.
    2. Group-query Attention (GQA): Described in the paper https://arxiv.org/pdf/2305.13245, `q_num_heads > kv_num_heads`, `q_num_heads % kv_num_heads == 0`.
    3. Multi-query Attention (MQA): Described in the paper https://arxiv.org/pdf/1911.02150, `q_num_heads > kv_num_heads`, `kv_num_heads=1`.

    Attention bias to be added is calculated based on ``attn_mask`` input and ``is_causal` `attribute``, only one of which can be provided.

    1. If ``is_causal`` is set to `1`, the attention masking is a lower triangular matrix when the mask is a square matrix. The attention masking has the form of the upper left causal bias due to the alignment.
    2. `attn_mask`: A boolean mask where a value of `True` indicates that the element should take part in attention or a float mask of the same type as query, key, value that is added to the attention score.

    Both past and present state key/values are optional. They shall be used together, and not allowed to use only one of them.
    The following pattern is applied to the Q, K and V inputs after appropriate reshaping of K and V inputs based on sequence lengths and num heads provided::

        The following pattern is applied by this operator:
                Q          K          V
                |          |          |
        Q*sqrt(scale) K*sqrt(scale) |
                |          |          |
                |       Transpose     |
                |          |          |
                ---MatMul---          |
                    |               |
        at_mask---Add              |
                    |               |
            softcap (if provided)     |
                    |               |
                Softmax            |
                    |               |
                    -----MatMul------
                            |
                            Y

    Args:
        Q: Query tensor. 4D tensor with shape `(batch_size, q_num_heads, q_sequence_length, head_size)` or 3D tensor
            with shape `(batch_size, q_sequence_length, q_hidden_size)`. For cases with a 3D input tensor,
            `q_hidden_size = q_num_heads * head_size`
        K: Key tensor. 4D tensor with shape `(batch_size, kv_num_heads, kv_sequence_length, head_size)` or 3D tensor
            with shape `(batch_size, kv_sequence_length, k_hidden_size)`. For cases with a 3D input tensor,
            `k_hidden_size = kv_num_heads * head_size`
        V: Value tensor. 4D tensor with shape `(batch_size, kv_num_heads, kv_sequence_length, v_head_size)` or 3D tensor
            with shape `(batch_size, kv_sequence_length, v_hidden_size)`. For cases with a 3D input tensor,
            `v_hidden_size = kv_num_heads * v_head_size`
        attn_mask: Attention mask. Shape must be broadcastable to 4D tensor with shape
            `(batch_size, q_num_heads, q_sequence_length, total_sequence_length)` where
            `total_sequence_length = past_sequence_length + kv_sequence_length`. Two types of masks are supported.
            A boolean mask where a value of True indicates that the element should take part in attention.
            Also supports a float mask of the same type as query, key, value that is added to the attention score.
        past_key: Past state cache for key with shape `(batch_size, kv_num_heads, past_sequence_length, head_size)`
        past_value: Past state cache for value with shape `(batch_size, kv_num_heads, past_sequence_length, v_head_size)`
        is_causal: If set to True, the attention masking is a lower triangular matrix when the mask is a square matrix.
            The attention masking has the form of the upper left causal bias due to the alignment.
        kv_num_heads: Number of heads of key and value. Must be used with 3D inputs of Q, K and V.
        q_num_heads: Number of heads of query. Must be used with 3D inputs of Q, K and V.
        qk_matmul_output_mode: If set to 0, qk_matmul_output is the output of qk matmul. If set to 1,
            qk_matmul_output includes the addition of the attention mask to the output of qk matmul.
            If set to 2, qk_matmul_output is the output after the softcap operation. If set to 3,
            qk_matmul_output is the output after the softmax operation. Default value is 0.
        scale: Scaling factor applied to Q*K^T. Default value is 1/sqrt(head_size). To prevent numerical overflow,
            scale Q, K by sqrt(scale) before matmul.
        softcap: Softcap value for attention weights. Default value is 0.
        softmax_precision: The floating-point precision used in softmax computation. If softmax precision is not provided,
            the same precision as the input of softmax (Q and K) is used.

    Returns:
        A tuple containing:
        - The output tensor. 4D tensor with shape `(batch_size, q_num_heads, q_sequence_length, v_head_size)` or 3D tensor
          with shape `(batch_size, q_sequence_length, hidden_size)`. For cases with a 3D input tensor,
          `hidden_size = q_num_heads * v_head_size`
        - Updated key cache with shape `(batch_size, kv_num_heads, total_sequence_length, head_size)` where
          `total_sequence_length = past_sequence_length + kv_sequence_length`.
        - Updated value cache with shape `(batch_size, kv_num_heads, total_sequence_length, v_head_size)` where
          `total_sequence_length = past_sequence_length + kv_sequence_length`.
        - The output of QK matmul. 4D tensor with shape `(batch_size, q_num_heads, q_sequence_length, total_sequence_length)`
          where `total_sequence_length = past_sequence_length + kv_sequence_length`.
    """
    return _impl.attention_23(
        Q,
        K,
        V,
        attn_mask=attn_mask,
        past_key=past_key,
        past_value=past_value,
        is_causal=is_causal,
        kv_num_heads=kv_num_heads,
        q_num_heads=q_num_heads,
        qk_matmul_output_mode=qk_matmul_output_mode,
        scale=scale,
        softcap=softcap,
        softmax_precision=softmax_precision,
    )


def attention(q, k, v, config: TuningConfig, save_residuals: bool = False):
  return _attention_forward(q, k, v, config, save_residuals)

