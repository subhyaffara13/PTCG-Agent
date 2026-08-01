
def sample_inputs_meshgrid(op_info: OpInfo, device: torch.device, dtype: torch.dtype,
                           requires_grad: bool,
                           *, variant: str, **kwargs) -> list[SampleInput]:
    if variant == 'variadic':
        def make_inputs(
                tensors: list[torch.Tensor]) -> tuple[torch.Tensor | list[torch.Tensor],
                                                      tuple[torch.Tensor, ...]]:
            return tensors
    elif variant == 'list':
        def make_inputs(
                tensors: list[torch.Tensor]) -> tuple[torch.Tensor | list[torch.Tensor],
                                                      tuple[torch.Tensor, ...]]:
            return [tensors]
    else:
        raise ValueError(
            'Unsupported variant, must be one of {"variadic", "list"}. '
            f'Got "{variant}".')

    SCALAR = torch.Size([])
    VECTOR = torch.Size([3])
    test_cases: list[list[torch.Size]] = [
        [SCALAR],
        [VECTOR],
        [VECTOR, SCALAR],
        [VECTOR, SCALAR, VECTOR],
        [VECTOR, SCALAR, VECTOR, SCALAR],
    ]

    for shapes, indexing in itertools.product(test_cases, {'xy', 'ij'}):
        args = make_inputs(
            [make_tensor(shape, dtype=dtype, device=device, requires_grad=requires_grad)
             for shape in shapes])
        yield SampleInput(*args, indexing=indexing)

