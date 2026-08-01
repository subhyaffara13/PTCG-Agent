
def _missing_raise():
    """Raise a ClusterError when called."""
    raise ClusterError("One of the clusters is empty. "
                       "Re-run kmeans with a different initialization.")

