
def mseloss_no_reduce_test():
    input_size = (2, 3, 4, 5)
    target = torch.randn(*input_size, dtype=torch.double)
    return dict(
        fullname='MSELoss_no_reduce',
        constructor=wrap_functional(
            lambda i: F.mse_loss(i, target.type_as(i), reduction='none')),
        cpp_function_call='F::mse_loss(i, target.to(i.options()), F::MSELossFuncOptions().reduction(torch::kNone))',
        input_size=input_size,
        cpp_var_map={'i': '_get_input()', 'target': target},
        reference_fn=lambda i, *_: (i - target).pow(2),
        supports_forward_ad=True,
        pickle=False,
        default_dtype=torch.double)

