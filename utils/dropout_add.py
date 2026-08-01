
def dropout_add(x: torch.Tensor, residual: torch.Tensor, prob: float, training: bool) -> torch.Tensor:
    """
    Dropout add function

    Args:
        x (`torch.tensor`):
            input tensor
        residual (`torch.tensor`):
            residual tensor
        prob (`float`):
            dropout probability
        training (`bool`):
            training mode
    """
    out = F.dropout(x, p=prob, training=training)
    out = residual + out
    return out


def dropout_add(x: torch.Tensor, residual: torch.Tensor, prob: float, training: bool) -> torch.Tensor:
    """
    Dropout add function

    Args:
        x (`torch.tensor`):
            input tensor
        residual (`torch.tensor`):
            residual tensor
        prob (`float`):
            dropout probability
        training (`bool`):
            training mode
    """
    out = F.dropout(x, p=prob, training=training)
    out = residual + out
    return out

