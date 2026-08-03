import random

def sample_inputs_huber_loss(op_info, device, dtype, requires_grad, **kwargs):
    for input, target, d in _generate_sample_inputs_nn_loss(op_info, device, dtype, requires_grad, **kwargs):
        d['delta'] = random.uniform(1e-3, 9)
        yield SampleInput(input, args=(target, ), kwargs=d)

