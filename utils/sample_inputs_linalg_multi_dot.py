
def sample_inputs_linalg_multi_dot(op_info, device, dtype, requires_grad, **kwargs):
    # Each test case consists of the sizes in the chain of multiplications
    # e.g. [2, 3, 4, 5] generates matrices (2, 3) @ (3, 4) @ (4, 5)
    test_cases = [
        [1, 2, 1],
        [2, 0, 2],
        [0, 2, 2],
        [2, 2, 2, 2],
        [2, 3, 4, 5],
        [5, 4, 0, 2],
        [2, 4, 3, 5, 3, 2],
    ]

    for sizes in test_cases:
        tensors = []
        for size in itertools.pairwise(sizes):
            t = make_tensor(
                size, dtype=dtype, device=device, requires_grad=requires_grad
            )
            tensors.append(t)
        yield SampleInput(tensors)

