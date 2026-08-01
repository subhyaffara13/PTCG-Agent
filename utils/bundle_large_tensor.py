
def bundle_large_tensor(t):
    """Wrap a tensor to allow bundling regardless of size."""
    return InflatableArg(value=t, fmt="{}")

