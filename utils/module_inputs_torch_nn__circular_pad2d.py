
def module_inputs_torch_nn_CircularPad2d(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    def padding2d_circular_ref(inp, pad):
        r"""input:
                [[[[0., 1., 2],
                   [3., 4., 5.]]]]
                pad: (1, 2, 2, 1)
        output:
            [[[[2., 0., 1., 2., 0., 1.],
               [5., 3., 4., 5., 3., 4.],
               [2., 0., 1., 2., 0., 1.],
               [5., 3., 4., 5., 3., 4.],
               [2., 0., 1., 2., 0., 1.]]]]
        """
        inp = torch.cat([inp[:, :, -pad[2]:], inp, inp[:, :, :pad[3]]], dim=2)
        return torch.cat([inp[:, :, :, -pad[0]:], inp, inp[:, :, :, :pad[1]]], dim=3)

    return [
        ModuleInput(
            constructor_input=FunctionInput(1),
            forward_input=FunctionInput(make_input((3, 4, 5))),
            reference_fn=no_batch_dim_reference_fn,
        ),
        ModuleInput(
            constructor_input=FunctionInput((1, 2, 2, 1)),
            forward_input=FunctionInput(make_input((1, 1, 2, 3))),
            reference_fn=lambda m, p, i: padding2d_circular_ref(i, m.padding),
        ),
        ModuleInput(
            constructor_input=FunctionInput((2, 3, 2, 2)),
            forward_input=FunctionInput(make_input((1, 1, 2, 3))),
            reference_fn=lambda m, p, i: padding2d_circular_ref(i, m.padding),
        ),
        ModuleInput(
            constructor_input=FunctionInput((3, 3, 3, 1)),
            forward_input=FunctionInput(make_input((1, 1, 3, 3))),
            reference_fn=lambda m, p, i: padding2d_circular_ref(i, m.padding),
        ),
    ]

