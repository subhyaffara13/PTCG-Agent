
def _disable_inference_mode() -> Generator[None, None, None]:
    # Disable inference_mode without clobbering grad_mode / fw_grad_mode.
    # torch.inference_mode(False) unconditionally sets grad_mode=True and
    # fw_grad_mode=True; we save and restore those to avoid that.
    # No-op when inference_mode is already off.
    if not torch.is_inference_mode_enabled():
        yield
        return
    prev_grad = torch.is_grad_enabled()
    prev_fw_grad = torch._C._is_fwd_grad_enabled()
    with torch.inference_mode(False):
        torch._C._set_grad_enabled(prev_grad)
        torch._C._set_fwd_grad_enabled(prev_fw_grad)
        yield

