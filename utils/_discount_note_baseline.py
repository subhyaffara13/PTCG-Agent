
def _discount_note_baseline(discount: float) -> str:
    """Same wording as harness.py; suppressed entirely when gamma == 1."""
    if discount >= 1.0:
        return ""
    return (
        f"  * Payoffs are discounted by a factor of {discount} per"
        " additional offer past the first. Accepting the very first"
        " offer is UNDISCOUNTED; if agreement is reached only after a"
        f" 2nd offer has been made, both players' payoffs are multiplied"
        f" by {discount}; after a 3rd offer, by {discount}^2; in"
        f" general, after the Nth offer, by {discount}^(N-1). Earlier"
        " acceptance preserves more reward.\n"
    )

