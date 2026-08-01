
def _kl_expfamily_expfamily(p, q):
    if type(p) is not type(q):
        raise NotImplementedError(
            "The cross KL-divergence between different exponential families cannot \
                            be computed using Bregman divergences"
        )
    p_nparams = [np.detach().requires_grad_() for np in p._natural_params]
    q_nparams = q._natural_params
    lg_normal = p._log_normalizer(*p_nparams)
    gradients = torch.autograd.grad(lg_normal.sum(), p_nparams, create_graph=True)
    result = q._log_normalizer(*q_nparams) - lg_normal
    for pnp, qnp, g in zip(p_nparams, q_nparams, gradients):
        term = (qnp - pnp) * g
        result -= _sum_rightmost(term, len(q.event_shape))
    return result

