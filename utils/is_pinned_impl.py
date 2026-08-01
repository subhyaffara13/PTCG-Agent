
def is_pinned_impl(self: ComplexTensor, device: torch.device | None = None) -> bool:
    return self.is_pinned(device)

