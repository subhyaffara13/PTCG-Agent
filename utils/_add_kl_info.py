
def _add_kl_info():
    """Appends a list of implemented KL functions to the doc for kl_divergence."""
    rows = [
        "KL divergence is currently implemented for the following distribution pairs:"
    ]
    for p, q in sorted(
        _KL_REGISTRY, key=lambda p_q: (p_q[0].__name__, p_q[1].__name__)
    ):
        rows.append(
            f"* :class:`~torch.distributions.{p.__name__}` and :class:`~torch.distributions.{q.__name__}`"
        )
    kl_info = "\n\t".join(rows)
    if kl_divergence.__doc__:
        # pyrefly: ignore [missing-attribute]
        kl_divergence.__doc__ += kl_info

