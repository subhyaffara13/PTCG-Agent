
def _default_apply_gate(self, gate_up_out: torch.Tensor) -> torch.Tensor:
    """
    Default gating mechanism: splits the gate_up_out into gate and up parts,
    applies the activation function to the gate part, and multiplies it with the up part.
    Args:
        gate_up_out (`torch.Tensor`):
            The output tensor from the gate and up projection of shape (S, 2 * intermediate_dim).
    Returns:
        `torch.Tensor`: The gated output tensor of shape (S, intermediate_dim).
    """
    gate, up = gate_up_out.chunk(2, dim=-1)  # (S, intermediate_dim)
    return self.act_fn(gate) * up  # (S, intermediate_dim)

