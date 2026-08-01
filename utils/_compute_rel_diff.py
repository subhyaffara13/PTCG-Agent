
def _compute_rel_diff(hash1, hash2):
    # Relative difference: |hash1 - hash2| / max(|hash1|, |hash2|, eps)
    numerator = abs(hash1 - hash2)
    denominator = max(abs(hash1), abs(hash2), 1e-10)
    return numerator / denominator

