
def log_sinkhorn_iterations(
    log_cost_matrix: torch.Tensor,
    log_source_distribution: torch.Tensor,
    log_target_distribution: torch.Tensor,
    num_iterations: int,
) -> torch.Tensor:
    """
    Perform Sinkhorn Normalization in Log-space for stability

    Args:
        log_cost_matrix (`torch.Tensor` of shape `(batch_size, num_rows, num_columns)`):
            Logarithm of the cost matrix.
        log_source_distribution (`torch.Tensor` of shape `(batch_size, num_rows)`):
            Logarithm of the source distribution.
        log_target_distribution (`torch.Tensor` of shape `(batch_size, num_columns)`):
            Logarithm of the target distribution.

    Returns:
        log_cost_matrix (`torch.Tensor` of shape `(batch_size, num_rows, num_columns)`): Logarithm of the optimal
        transport matrix.
    """
    log_u_scaling = torch.zeros_like(log_source_distribution)
    log_v_scaling = torch.zeros_like(log_target_distribution)
    for _ in range(num_iterations):
        log_u_scaling = log_source_distribution - torch.logsumexp(log_cost_matrix + log_v_scaling.unsqueeze(1), dim=2)
        log_v_scaling = log_target_distribution - torch.logsumexp(log_cost_matrix + log_u_scaling.unsqueeze(2), dim=1)
    return log_cost_matrix + log_u_scaling.unsqueeze(2) + log_v_scaling.unsqueeze(1)

