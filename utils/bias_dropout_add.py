
def bias_dropout_add(x: Tensor, bias: Tensor, residual: Tensor | None, prob: float, training: bool) -> Tensor:
    """add bias to x, apply dropout and residual connection

    Args:
        x (Tensor): main path of output
        bias (Tensor): None or attn_bias of the last attention layer
        residual (Optional[Tensor]): residual value
        prob (float): dropout probability
        training (bool): whether in training mode or not

    Returns:
        Tensor: dropout(x + bias) + residual
    """
    if bias is not None:
        x = x + bias
    out = torch.nn.functional.dropout(x, p=prob, training=training)
    if residual is not None:
        out = residual + out
    return out

