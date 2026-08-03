import random

def sample_inputs_hinge_embedding_loss(op_info, device, dtype, requires_grad, **kwargs):
    for input, target, d in _generate_sample_inputs_nn_loss(op_info, device, dtype, requires_grad, **kwargs):
        # target should contain either 1 or -1 as per docs
        mask = torch.rand_like(target) > 0.5
        target[mask] = 1
        target[~mask] = -1
        d['margin'] = random.uniform(-9, 9)
        yield SampleInput(input, args=(target, ), kwargs=d)

    # scalar input and target.
    _make_tensor = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    yield SampleInput(_make_tensor(()), args=(_make_tensor(()), ))

