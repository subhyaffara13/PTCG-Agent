
def sample_inputs_scatter_add(op_info, device, dtype, requires_grad, **kwargs):
    def _tensor(shape, dtype=dtype, low=None, high=None):
        return make_tensor(shape, dtype=dtype, device=device, low=low, high=high, requires_grad=requires_grad)

    def _gather(shape, index_dim, max_indices):
        return gather_variable(shape, index_dim, max_indices, device=device)

    zero = torch.tensor(0, dtype=torch.long, device=device)
    yield SampleInput(_tensor((M, S)), 0, _gather((S, S), 1, M), _tensor((S, S)))
    yield SampleInput(_tensor((M, S)), 1, _gather((S, S), 0, S), _tensor((S, S)))
    yield SampleInput(_tensor((M, S)), -1, _gather((S, S), 0, S), _tensor((S, S)))
    yield SampleInput(_tensor((M, S)), 0, _gather((M, S // 2), 1, M), _tensor((M, S // 2)))
    yield SampleInput(_tensor((M, S)), 1, _gather((M, S // 2), 0, S), _tensor((M, S // 2)))
    yield SampleInput(_tensor((M, S)), -1, _gather((M, S // 2), 0, S), _tensor((M, S // 2)))
    yield SampleInput(_tensor(()), 0, zero.detach().clone(), _tensor(()))

