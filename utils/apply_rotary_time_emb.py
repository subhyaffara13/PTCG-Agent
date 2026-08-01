
def apply_rotary_time_emb(hidden_states, cos, sin):
    original_dtype = hidden_states.dtype
    hidden_states = hidden_states.to(torch.float64)
    cos = cos.to(hidden_states)
    sin = sin.to(hidden_states)
    rot_dim = cos.shape[-1]

    passthrough = hidden_states[..., rot_dim:]
    rotated = hidden_states[..., :rot_dim]
    rotated = (rotated * cos) + (rotate_half(rotated) * sin)
    return torch.cat((rotated, passthrough), dim=-1).to(original_dtype)


def apply_rotary_time_emb(hidden_states, cos, sin):
    original_dtype = hidden_states.dtype
    hidden_states = hidden_states.to(torch.float64)
    cos = cos.to(hidden_states)
    sin = sin.to(hidden_states)
    rot_dim = cos.shape[-1]

    passthrough = hidden_states[..., rot_dim:]
    rotated = hidden_states[..., :rot_dim]
    rotated = (rotated * cos) + (rotate_half(rotated) * sin)
    return torch.cat((rotated, passthrough), dim=-1).to(original_dtype)

