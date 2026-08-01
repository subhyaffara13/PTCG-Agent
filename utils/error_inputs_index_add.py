
def error_inputs_index_add(op_info, device, **kwargs):
    result = torch.tensor([[1., 2.], [4., 5.], [7., 8.]])
    source = torch.tensor([2., 4.])

    yield ErrorInput(SampleInput(result, args=(0, torch.tensor([0, 2]), source)),
                     error_type=RuntimeError,
                     error_regex=r'source tensor shape must match self tensor shape, '
                     r'excluding the specified dimension. Got self.shape = \[3, 2\] source.shape = \[2\]')

