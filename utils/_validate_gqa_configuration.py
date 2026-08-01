
def _validate_gqa_configuration(
    current_q_num_heads: int, current_kv_num_heads: int
) -> None:
    """Validate Group Query Attention configuration."""
    torch._check(
        current_q_num_heads % current_kv_num_heads == 0,
        lambda: f"q_num_heads ({current_q_num_heads}) must be divisible by kv_num_heads ({current_kv_num_heads}) for GQA",
    )

