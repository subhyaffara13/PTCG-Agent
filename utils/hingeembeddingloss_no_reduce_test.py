
def hingeembeddingloss_no_reduce_test():
    t = Variable(torch.randn(10).gt(0).to(torch.double).mul_(2).sub(1))
    return dict(
        fullname='HingeEmbeddingLoss_no_reduce',
        constructor=wrap_functional(
            lambda i: F.hinge_embedding_loss(i, t.type_as(i), reduction='none')),
        cpp_function_call='''F::hinge_embedding_loss(
            i, t.to(i.options()), F::HingeEmbeddingLossFuncOptions().reduction(torch::kNone))''',
        input_fn=lambda: torch.randn(10),
        cpp_var_map={'i': '_get_input()', 't': t},
        reference_fn=lambda i, *_:
            loss_reference_fns['HingeEmbeddingLoss'](i, t.type_as(i), reduction='none'),
        check_sum_reduction=True,
        pickle=False,
        default_dtype=torch.double)

