
def _csv_transformer(value: str) -> Sequence[str]:
    """Transforms a comma separated string."""
    return pylint_utils._check_csv(value)

