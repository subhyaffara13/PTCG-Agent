
def sample_inputs_topk(op_info, device, dtype, requires_grad, **kwargs):
    def get_tensor_input(size):
        return make_tensor(size, dtype=dtype, device=device, requires_grad=requires_grad)

    yield SampleInput(get_tensor_input((S, M, S)), 3)
    yield SampleInput(get_tensor_input((S, M, S)), 3, 1)
    yield SampleInput(get_tensor_input((S, M, S)), 3, -2)
    yield SampleInput(get_tensor_input((S, M, S)), 3, 1, True)
    yield SampleInput(get_tensor_input((S, M, S)), 3, -2, True)
    yield SampleInput(get_tensor_input((S, M, S)), 3, 1, True, True)
    yield SampleInput(get_tensor_input((S, M, S)), 3, -2, True, True)

    yield SampleInput(get_tensor_input(()), 1)
    yield SampleInput(get_tensor_input(()), 1, 0)
    yield SampleInput(get_tensor_input(()), 1, -1)
    yield SampleInput(get_tensor_input(()), 1, 0, True)
    yield SampleInput(get_tensor_input(()), 1, -1, True)
    yield SampleInput(get_tensor_input(()), 1, 0, True, True)
    yield SampleInput(get_tensor_input(()), 1, -1, True, True)

