
def huberloss_delta_test():
    t = torch.randn(2, 3, 4)
    return dict(
        fullname='HuberLoss_delta',
        constructor=wrap_functional(
            lambda i: F.huber_loss(i, t.type_as(i), reduction='none', delta=0.5)),
        cpp_function_call='''F::huber_loss(
            i, t.to(i.options()), F::HuberLossFuncOptions().reduction(torch::kNone).delta(0.5))''',
        input_fn=lambda: torch.randn(2, 3, 4),
        cpp_var_map={'i': '_get_input()', 't': t},
        reference_fn=lambda i, *_:
            loss_reference_fns['HuberLoss'](i, t.type_as(i), reduction='none', delta=0.5),
        supports_forward_ad=True,
        pickle=False,
        default_dtype=torch.double)

