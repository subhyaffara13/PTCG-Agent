
def _merge_beta_headers(existing: Optional[str], new_beta: str) -> str:
    """Merge a new beta value into an existing comma-separated anthropic-beta header."""
    if not existing:
        return new_beta
    betas = {b.strip() for b in existing.split(",") if b.strip()}
    betas.add(new_beta)
    return ",".join(sorted(betas))

