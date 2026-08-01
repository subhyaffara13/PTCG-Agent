
def error_inputs_neg(op_info, device, **kwargs):
    si = SampleInput(torch.tensor((False, True), device=device))
    msg = ("Negation, the `\\-` operator, on a bool tensor is not supported."
           " If you are trying to invert a mask, use the `\\~` or"
           " `logical_not\\(\\)` operator instead.")
    yield ErrorInput(si, error_regex=msg)

