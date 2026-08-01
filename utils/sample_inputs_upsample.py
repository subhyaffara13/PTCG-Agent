
def sample_inputs_upsample(mode, self, device, dtype, requires_grad, **kwargs):
    N, C = 2, 3
    D = 4
    S = 3
    L = 5

    ranks_for_mode = {
        'nearest': [1, 2, 3],
        'bilinear': [2],
    }

    def shape(size, rank, with_batch_channel=True):
        if with_batch_channel:
            return torch.Size([N, C] + ([size] * rank))
        return torch.Size([size] * rank)

    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    for rank in ranks_for_mode[mode]:
        yield SampleInput(make_arg(shape(D, rank)), size=shape(S, rank, False))
        yield SampleInput(make_arg(shape(D, rank)), size=shape(L, rank, False))
        yield SampleInput(make_arg(shape(D, rank)), scale_factor=1.7)
        yield SampleInput(make_arg(shape(D, rank)), scale_factor=0.6)

