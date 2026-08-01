
def recompute_mean_var(
    input: Tensor, rstd: Tensor, inner_dim_indices: list[int], keepdim: bool
):
    # for most norm decompositions, it will be the same as the core version except for here.
    # We recompute the mean and variance so that they track gradients through input

    mean = torch.mean(input, dim=inner_dim_indices, keepdim=keepdim)
    var = torch.var(input, dim=inner_dim_indices, unbiased=False, keepdim=keepdim)
    eps = torch.pow(1 / rstd, 2) - var  # this makes me so sad inside
    eps = eps.detach()
    rstd = 1 / torch.sqrt(var + eps)
    return mean, rstd

