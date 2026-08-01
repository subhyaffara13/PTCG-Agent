
def bceloss_no_reduce_scalar_test():
    t = torch.randn(()).gt(0).to(torch.double)
    return dict(
        fullname='BCELoss_no_reduce_scalar',
        constructor=wrap_functional(
            lambda i: F.binary_cross_entropy(i, t.type_as(i), reduction='none')),
        cpp_function_call='F::binary_cross_entropy('
                          'i, t.to(i.options()), F::BinaryCrossEntropyFuncOptions().reduction(torch::kNone))',
        input_fn=lambda: torch.rand(()).clamp_(2.8e-2, 1 - 2.8e-2),
        cpp_var_map={'i': '_get_input()', 't': t},
        reference_fn=lambda i, *_: -(t * i.log() + (1 - t) * (1 - i).log()),
        pickle=False,
        default_dtype=torch.double)

