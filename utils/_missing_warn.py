
def _missing_warn():
    """Print a warning when called."""
    warnings.warn("One of the clusters is empty. "
                  "Re-run kmeans with a different initialization.",
                  stacklevel=3)

