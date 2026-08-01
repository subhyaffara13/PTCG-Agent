
def is_parameter_freezing() -> bool:
    return torch._inductor.config.freezing and not torch.is_grad_enabled()

