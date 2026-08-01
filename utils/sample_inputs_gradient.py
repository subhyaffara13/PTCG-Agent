
def sample_inputs_gradient(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad, low=None, high=None)
    test_cases_float = (
        ((S,), None, None, 1),
        ((S,), 2., None, 1),
        ((S, S), None, None, 2),
        ((S, S), [2.0, 2.1], None, 1),
        ((S, S), [2.0, 2.1], (0, 1), 1),
        ((4, 4, 4), [2., 1.], (0, 1), 2),
    )
    for size, spacing, dim, edge_order in test_cases_float:
        t = make_arg(size)
        yield SampleInput(t, dim=dim, spacing=spacing, edge_order=edge_order)

    test_cases_tensor = (
        ((3, 3, 3), ((1.1, 2.0, 3.5), (4.0, 2, 6.0)), (0, -1), 1),
        ((3, 3, 3), ((1.0, 3.0, 2.0), (8.0, 6.0, 1.0)), (0, 1), 2),
    )
    for size, coordinates, dim, edge_order in test_cases_tensor:
        t = make_arg(size)
        coordinates_tensor_list = []
        for coords in coordinates:
            a = torch.tensor(coords, device=device, dtype=dtype)
            coordinates_tensor_list.append(a)
        yield SampleInput(t, dim=dim, spacing=coordinates_tensor_list, edge_order=edge_order)

