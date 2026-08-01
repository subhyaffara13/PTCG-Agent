
def non_cont_test(t_view, t_cont):
    if t_view.is_contiguous():
        raise Exception("t_view is contiguous!")  # noqa: TRY002
    if not t_cont.is_contiguous():
        raise Exception("t_cont is not contiguous!")  # noqa: TRY002
    if not torch.equal(t_view, t_cont):
        raise Exception("t_view is not equal to t_cont!")  # noqa: TRY002
    return t_view

