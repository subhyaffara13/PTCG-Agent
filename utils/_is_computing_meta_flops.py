
def _is_computing_meta_flops(x):
    # Note: there's a use case of using meta tensors & the dispatch-based flop counter.
    # We can use this function to check for this scenario in order to handle it specially.
    if not torch.jit.is_scripting() and x.device.type == "meta":
        torch_dispatch_mode_stack = (
            torch.utils._python_dispatch._get_current_dispatch_mode_stack()
        )
        return any(
            type(x) is torch.utils.flop_counter._FlopCounterMode
            for x in torch_dispatch_mode_stack
        )
    return False

