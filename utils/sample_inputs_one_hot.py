
def sample_inputs_one_hot(op_info, device, dtype, requires_grad, **kwargs):
    def make_input(shape, *, low, high):
        return make_tensor(shape, device=device, dtype=dtype, low=low, high=high, requires_grad=requires_grad)

    shapes = ((), (S,), (L, M, S))
    num_classess = (-1, 10)

    return (
        SampleInput(
            make_input(
                shape,
                low=0,
                high=10 if num_classes == -1 else num_classes // 2,
            ),
            kwargs=dict(num_classes=num_classes),
        )
        for shape, num_classes in itertools.product(shapes, num_classess)
    )

