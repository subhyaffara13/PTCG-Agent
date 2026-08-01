
def _estimate_batch_entry_tokens(raw_line: bytes) -> int:
    """Conservative token estimate for a batch row the token counter cannot measure
    (or that cannot be parsed). Keeps the batch token total non-zero so a crafted
    row cannot evade the TPM limit, without hard-rejecting a legitimate batch."""
    return max(1, len(raw_line) // _BATCH_TOKEN_ESTIMATE_BYTES_PER_TOKEN)

