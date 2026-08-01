
def bundle_randn(*size, dtype=None):
    """Generate a tensor that will be inflated with torch.randn."""
    stub = torch.zeros(1, dtype=dtype).expand(*size)
    return InflatableArg(value=stub, fmt="torch.randn_like({})")

