
def int_pos_callback(ctx: MethodContext) -> Type:
    """Infer a more precise return type for int.__pos__.

    This is identical to __neg__, except the value is not inverted.
    """
    return int_neg_callback(ctx, +1)

