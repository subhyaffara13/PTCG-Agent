
def set_warn_always_context(new_val: bool):
    old_val = torch.is_warn_always_enabled()
    torch.set_warn_always(new_val)
    try:
        yield
    finally:
        torch.set_warn_always(old_val)

