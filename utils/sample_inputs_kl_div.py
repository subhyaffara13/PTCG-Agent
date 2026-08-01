
def sample_inputs_kl_div(op_info, device, dtype, requires_grad, **kwargs):
    # kl_div works with inputs in [0, 1] (aka the pdf of a probability measure)
    # Then log [0, 1] = (-inf, 0], so this is the log space
    make_arg = partial(make_tensor, low=0., device=device, dtype=dtype, requires_grad=requires_grad)

    def make_log(shape):
        out = torch.nn.functional.log_softmax(make_arg(shape), -1)
        out.requires_grad_(requires_grad)
        return out

    def make_prob(shape):
        out = torch.nn.functional.softmax(make_arg(shape), -1)
        out.requires_grad_(requires_grad)
        return out

    shapes = ((2,), (2, 3))
    reductions = ("none", "mean", "batchmean", "sum")
    for shape, reduction, log_target in product(shapes, reductions, (True, False)):
        input = make_log(shape)
        target = make_log(shape) if log_target else make_prob(shape)
        yield SampleInput(input, args=(target,), kwargs=dict(reduction=reduction, log_target=log_target))

