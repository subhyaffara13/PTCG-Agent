
def multimarginloss_margin_no_reduce_test():
    t = torch.rand(5).mul(8).floor().long()
    return dict(
        fullname='MultiMarginLoss_margin_no_reduce',
        constructor=wrap_functional(
            lambda i: F.multi_margin_loss(i, t.type_as(i).long(), margin=0.5, reduction='none')),
        cpp_function_call='''F::multi_margin_loss(
            i, t.to(i.options()).to(torch::kLong),
            F::MultiMarginLossFuncOptions().margin(0.5).reduction(torch::kNone))''',
        input_fn=lambda: torch.randn(5, 10),
        cpp_var_map={'i': '_get_input()', 't': t},
        reference_fn=lambda i, *_:
            loss_reference_fns['MultiMarginLoss'](i, t.data.type_as(i).long(),
                                                  margin=0.5, reduction='none'),
        check_sum_reduction=True,
        check_gradgrad=False,
        pickle=False,
        default_dtype=torch.double)

