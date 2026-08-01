
def smoothl1loss_beta_test():
    t = torch.randn(2, 3, 4, dtype=torch.double)
    return dict(
        fullname='SmoothL1Loss_beta',
        constructor=wrap_functional(
            lambda i: F.smooth_l1_loss(i, t.type_as(i), reduction='none', beta=0.5)),
        cpp_function_call='''F::smooth_l1_loss(
            i, t.to(i.options()), F::SmoothL1LossFuncOptions().reduction(torch::kNone), 0.5)''',
        input_fn=lambda: torch.randn(2, 3, 4),
        cpp_var_map={'i': '_get_input()', 't': t},
        reference_fn=lambda i, *_:
            loss_reference_fns['SmoothL1Loss'](i, t.type_as(i), reduction='none', beta=0.5),
        supports_forward_ad=True,
        pickle=False,
        default_dtype=torch.double)

