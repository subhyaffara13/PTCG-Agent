
def sparsemixer(scores, jitter_eps, training, top_k=2):
    """
    Sparse mixer function to select top-k experts and compute multipliers.
    Based on the paper: https://huggingface.co/papers/2409.12136
    We first replace the TopK(·) function as random sampling of discrete variables
    in model training. Then, following Liu et al. (2023a) and Liu et al. (2023b), we apply Heun's
    third order method to approximate the expert routing gradient and construct a modified
    back-propagation to give a mathematically sound gradient estimation for expert routing.

    Args:
        scores (torch.Tensor): Input scores tensor.
        jitter_eps (float): Jitter epsilon for numerical stability.
        training (bool): Flag indicating if the model is in training mode.
        top_k (int): Number of top experts to select.

    Returns:
        tuple[torch.Tensor, torch.Tensor]: Multiplier and selected experts tensors.
    """
    with torch.no_grad():
        # Compute mask for sparsity
        mask_logits_threshold, max_ind = scores.max(dim=-1, keepdim=True)
        factor = scores.abs().clamp(min=mask_logits_threshold)
        mask_logits_threshold = ((mask_logits_threshold - scores) / factor) > (2 * jitter_eps)

    # Apply mask
    masked_gates = scores.masked_fill(mask_logits_threshold, float("-inf"))
    if training:
        selected_experts = (
            (
                masked_gates
                - torch.empty_like(masked_gates, memory_format=torch.legacy_contiguous_format).exponential_().log()
            )
            .max(dim=-1)[1]
            .unsqueeze(-1)
        )  # Gumbel sampling, more robust than the multinomial method
    else:
        selected_experts = max_ind

    # Compute scores for gradients
    masked_gates = torch.softmax(masked_gates, dim=-1)
    multiplier_o = masked_gates.gather(dim=-1, index=selected_experts)

    if training:
        # Compute midpoint mask
        max_scores, max_ind = masked_gates.max(dim=-1, keepdim=True)
        mask_for_one = torch.logical_or(
            selected_experts == max_ind,
            torch.rand_like(max_scores) > 0.75,  # Heun's third-order method
        )
        # 1 -> 1.0 & 0 -> 1./3: lambda x: (x + 0.5) / 1.5
        mask_for_one = torch.add(0.3333, mask_for_one, alpha=0.6667).type_as(masked_gates)

        multiplier = PhimoeMultiplier.apply(
            scores,
            multiplier_o,
            selected_experts,
            masked_gates,
            mask_for_one,
        )
    else:
        multiplier = multiplier_o

    # Masked out first expert
    masked_scores = torch.scatter(
        scores,
        -1,
        selected_experts,
        float("-inf"),
    )
    with torch.no_grad():
        # Compute mask for sparsity
        mask_logits_threshold, max_ind = masked_scores.max(dim=-1, keepdim=True)
        factor = scores.abs().clamp(min=mask_logits_threshold)
        mask_logits_threshold = ((mask_logits_threshold - scores) / factor) > (2 * jitter_eps)

    # Apply mask
    masked_gates_top2 = masked_scores.masked_fill(mask_logits_threshold, float("-inf"))
    if training:
        selected_experts_top2 = (
            (
                masked_gates_top2
                - torch.empty_like(masked_gates_top2, memory_format=torch.legacy_contiguous_format)
                .exponential_()
                .log()
            )
            .max(dim=-1)[1]
            .unsqueeze(-1)
        )  # Gumbel sampling, more robust than the multinomial method
    else:
        selected_experts_top2 = max_ind
    # Compute scores for gradients
    masked_gates_top2 = torch.softmax(masked_gates_top2, dim=-1)
    multiplier_top2_o = masked_gates_top2.gather(dim=-1, index=selected_experts_top2)

    if training:
        # Compute midpoint mask
        max_scores, max_ind = masked_gates_top2.max(dim=-1, keepdim=True)
        mask_for_one_top2 = torch.logical_or(
            selected_experts_top2 == max_ind,
            torch.rand_like(max_scores).uniform_() > 0.75,  # Heun's third-order method
        )
        # 1 -> 1.0 & 0 -> 1./3: lambda x: (x + 0.5) / 1.5
        mask_for_one_top2 = torch.add(0.3333, mask_for_one_top2, alpha=0.6667).type_as(masked_gates_top2)

        multiplier_top2 = PhimoeMultiplier.apply(
            scores,
            multiplier_top2_o,
            selected_experts_top2,
            masked_gates_top2,
            mask_for_one_top2,
        )
    else:
        multiplier_top2 = multiplier_top2_o

    multiplier = torch.concat((multiplier, multiplier_top2), dim=-1)
    selected_experts = torch.concat((selected_experts, selected_experts_top2), dim=-1)

    return (
        multiplier,
        selected_experts,
    )


def sparsemixer(scores, jitter_eps, training, top_k=2):
    """
    Sparse mixer function to select top-k experts and compute multipliers.
    Based on the paper: https://huggingface.co/papers/2409.12136
    We first replace the TopK(·) function as random sampling of discrete variables
    in model training. Then, following Liu et al. (2023a) and Liu et al. (2023b), we apply Heun's
    third order method to approximate the expert routing gradient and construct a modified
    back-propagation to give a mathematically sound gradient estimation for expert routing.

    Args:
        scores (torch.Tensor): Input scores tensor.
        jitter_eps (float): Jitter epsilon for numerical stability.
        training (bool): Flag indicating if the model is in training mode.
        top_k (int): Number of top experts to select.

    Returns:
        tuple[torch.Tensor, torch.Tensor]: Multiplier and selected experts tensors.
    """
    with torch.no_grad():
        # Compute mask for sparsity
        mask_logits_threshold, max_ind = scores.max(dim=-1, keepdim=True)
        factor = scores.abs().clamp(min=mask_logits_threshold)
        mask_logits_threshold = ((mask_logits_threshold - scores) / factor) > (2 * jitter_eps)

    # Apply mask
    masked_gates = scores.masked_fill(mask_logits_threshold, float("-inf"))
    if training:
        selected_experts = (
            (
                masked_gates
                - torch.empty_like(masked_gates, memory_format=torch.legacy_contiguous_format).exponential_().log()
            )
            .max(dim=-1)[1]
            .unsqueeze(-1)
        )  # Gumbel sampling, more robust than the multinomial method
    else:
        selected_experts = max_ind

    # Compute scores for gradients
    masked_gates = torch.softmax(masked_gates, dim=-1)
    multiplier_o = masked_gates.gather(dim=-1, index=selected_experts)

    if training:
        # Compute midpoint mask
        max_scores, max_ind = masked_gates.max(dim=-1, keepdim=True)
        mask_for_one = torch.logical_or(
            selected_experts == max_ind,
            torch.rand_like(max_scores) > 0.75,  # Heun's third-order method
        )
        # 1 -> 1.0 & 0 -> 1./3: lambda x: (x + 0.5) / 1.5
        mask_for_one = torch.add(0.3333, mask_for_one, alpha=0.6667).type_as(masked_gates)

        multiplier = PhimoeMultiplier.apply(
            scores,
            multiplier_o,
            selected_experts,
            masked_gates,
            mask_for_one,
        )
    else:
        multiplier = multiplier_o

    # Masked out first expert
    masked_scores = torch.scatter(
        scores,
        -1,
        selected_experts,
        float("-inf"),
    )
    with torch.no_grad():
        # Compute mask for sparsity
        mask_logits_threshold, max_ind = masked_scores.max(dim=-1, keepdim=True)
        factor = scores.abs().clamp(min=mask_logits_threshold)
        mask_logits_threshold = ((mask_logits_threshold - scores) / factor) > (2 * jitter_eps)

    # Apply mask
    masked_gates_top2 = masked_scores.masked_fill(mask_logits_threshold, float("-inf"))
    if training:
        selected_experts_top2 = (
            (
                masked_gates_top2
                - torch.empty_like(masked_gates_top2, memory_format=torch.legacy_contiguous_format)
                .exponential_()
                .log()
            )
            .max(dim=-1)[1]
            .unsqueeze(-1)
        )  # Gumbel sampling, more robust than the multinomial method
    else:
        selected_experts_top2 = max_ind
    # Compute scores for gradients
    masked_gates_top2 = torch.softmax(masked_gates_top2, dim=-1)
    multiplier_top2_o = masked_gates_top2.gather(dim=-1, index=selected_experts_top2)

    if training:
        # Compute midpoint mask
        max_scores, max_ind = masked_gates_top2.max(dim=-1, keepdim=True)
        mask_for_one_top2 = torch.logical_or(
            selected_experts_top2 == max_ind,
            torch.rand_like(max_scores).uniform_() > 0.75,  # Heun's third-order method
        )
        # 1 -> 1.0 & 0 -> 1./3: lambda x: (x + 0.5) / 1.5
        mask_for_one_top2 = torch.add(0.3333, mask_for_one_top2, alpha=0.6667).type_as(masked_gates_top2)

        multiplier_top2 = PhimoeMultiplier.apply(
            scores,
            multiplier_top2_o,
            selected_experts_top2,
            masked_gates_top2,
            mask_for_one_top2,
        )
    else:
        multiplier_top2 = multiplier_top2_o

    multiplier = torch.concat((multiplier, multiplier_top2), dim=-1)
    selected_experts = torch.concat((selected_experts, selected_experts_top2), dim=-1)

    return (
        multiplier,
        selected_experts,
    )

