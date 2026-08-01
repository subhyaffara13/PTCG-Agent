
def rms_forward(hidden_states, variance_epsilon=1e-6):
    """
    Calculates simple RMSNorm with no learnable weights. `MambaRMSNorm` will
    leverage this in order to multiply the final result with the RMSNorm weight

    Args:
        hidden_states (`torch.Tensor`):
            Hidden states to normalize
        variance_epsilon (`float`):
            The eps value to add in the square root scaling factor
    """
    input_dtype = hidden_states.dtype
    hidden_states = hidden_states.to(torch.float32)

    variance = hidden_states.pow(2).mean(-1, keepdim=True)
    hidden_states = hidden_states * torch.rsqrt(variance + variance_epsilon)
    return hidden_states.to(input_dtype)


def rms_forward(hidden_states, variance_epsilon=1e-6):
    """
    Calculates simple RMSNorm with no learnable weights. `MambaRMSNorm` will
    leverage this in order to multiply the final result with the RMSNorm weight

    Args:
        hidden_states (`torch.Tensor`):
            Hidden states to normalize
        variance_epsilon (`float`):
            The eps value to add in the square root scaling factor
    """
    input_dtype = hidden_states.dtype
    hidden_states = hidden_states.to(torch.float32)

    variance = hidden_states.pow(2).mean(-1, keepdim=True)
    hidden_states = hidden_states * torch.rsqrt(variance + variance_epsilon)
    return hidden_states.to(input_dtype)

