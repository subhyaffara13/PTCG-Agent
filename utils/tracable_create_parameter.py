
def tracable_create_parameter(
    tensor: torch.Tensor, placeholder: torch.nn.Parameter
) -> torch.nn.Parameter:
    with torch.set_grad_enabled(placeholder.requires_grad):
        out = TracableCreateParameter.apply(tensor, placeholder)
    return out

