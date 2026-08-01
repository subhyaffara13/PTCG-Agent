
def smoothl1loss_no_reduce_scalar_test():
    t = torch.randn((), dtype=torch.double)
    return dict(
        fullname='SmoothL1Loss_no_reduce_scalar',
        constructor=wrap_functional(
            lambda i: F.smooth_l1_loss(i, t.type_as(i), reduction='none')),
        cpp_function_call='''F::smooth_l1_loss(
            i, t.to(i.options()), F::SmoothL1LossFuncOptions().reduction(torch::kNone))''',
        input_fn=lambda: torch.randn(()),
        cpp_var_map={'i': '_get_input()', 't': t},
        reference_fn=lambda i, *_:
            loss_reference_fns['SmoothL1Loss'](i, t.type_as(i), reduction='none'),
        supports_forward_ad=True,
        pickle=False,
        default_dtype=torch.double)

