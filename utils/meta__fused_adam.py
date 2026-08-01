
def meta__fused_adam(
    self,
    grads,
    exp_avgs,
    exp_avg_sqs,
    max_exp_avg_sqs,
    state_steps,
    *,
    lr,
    beta1,
    beta2,
    weight_decay,
    eps,
    amsgrad,
    maximize,
    grad_scale=None,
    found_inf=None,
):
    for l in [self, grads, exp_avgs, exp_avg_sqs, max_exp_avg_sqs, state_steps]:
        torch._check(
            isinstance(l, list),
            lambda: f"exponent must be a tensor list but got {type(l)}",
        )

    def empty_like_list(tensor_list):
        return [torch.empty_like(t) for t in tensor_list]

    return (
        empty_like_list(self),
        empty_like_list(grads),
        empty_like_list(exp_avgs),
        empty_like_list(exp_avg_sqs),
        empty_like_list(max_exp_avg_sqs),
    )

