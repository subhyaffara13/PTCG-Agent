
def clone_sample(sample, **kwargs):
    """
    Given a SampleInput, this function analyzes its input, args and kwargs,
    and produces a copy with each non-Tensor entry being copied by reference,
    and with each Tensor entry cloned with `t.clone().requires_grad_(t.requires_grad)`
    """

    def clone_tensor(t):
        if isinstance(t, torch.Tensor):
            return t.detach().clone().requires_grad_(t.requires_grad)
        else:
            return t

    sample_kwargs = kwargs if kwargs else sample.kwargs

    return SampleInput(
        clone_tensor(sample.input),
        args=tuple(map(clone_tensor, sample.args)),
        kwargs={k: clone_tensor(v) for k, v in sample_kwargs.items()},
    )

