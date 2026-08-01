
def get_ema_avg_fn(decay=0.999):
    """Get the function applying exponential moving average (EMA) across multiple params.

    The EMA is computed as:

    .. math::
        W_0^{\\text{EMA}} = W_0^{\\text{model}}

    .. math::
        W_{t+1}^{\\text{EMA}} = \\text{decay} \\times W_t^{\\text{EMA}} + (1 - \\text{decay}) \\times W_{t+1}^{\\text{model}}

    where :math:`W_t^{\\text{EMA}}` is the EMA parameter at step :math:`t`,
    :math:`W_t^{\\text{model}}` is the model parameter at step :math:`t`,
    and :math:`\\text{decay}` is the decay rate (default: 0.999).

    Args:
        decay (float): Decay rate for EMA. Must be in the range [0, 1]. Default: 0.999

    Returns:
        Callable: A function that updates EMA parameters given current model parameters
    """

    if decay < 0.0 or decay > 1.0:
        raise ValueError(
            f"Invalid decay value {decay} provided. Please provide a value in [0,1] range."
        )

    @torch.no_grad()
    def ema_update(ema_param: Tensor, current_param: Tensor, num_averaged):
        return decay * ema_param + (1 - decay) * current_param

    return ema_update

