
def fill_with_neg_inf(t):
    """FP16-compatible function that fills a input_ids with -inf."""
    return t.float().fill_(torch.finfo(t.dtype).min).type_as(t)

