import random

def sample_inputs_cosine_embedding_loss(op_info, device, dtype, requires_grad, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    def make_target(shape):
        shape = () if len(shape) == 1 else (shape[0], )
        t = torch.randint(0, 2, shape, device=device, dtype=torch.long)
        # Label with -1 or 1
        t = t * 2 - 1
        target = t.to(dtype=dtype).detach_().requires_grad_(requires_grad)
        return target

    shapes = ((S, S), (S,))
    reductions = ('none', 'mean', 'sum')
    for s, r in product(shapes, reductions):
        yield SampleInput(
            make_input(s),
            args=(make_input(s), make_target(s)),
            kwargs=dict(reduction=r, margin=random.uniform(-1, 1))
        )

