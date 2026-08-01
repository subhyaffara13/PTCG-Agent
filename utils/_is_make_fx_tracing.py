
def _is_make_fx_tracing():
    if not torch.jit.is_scripting():
        torch_dispatch_mode_stack = (
            torch.utils._python_dispatch._get_current_dispatch_mode_stack()
        )
        # this can be triggered when dynamo inlining the module too.
        return (
            any(
                type(x) is torch.fx.experimental.proxy_tensor.ProxyTorchDispatchMode
                for x in torch_dispatch_mode_stack
            )
            or torch.compiler.is_exporting()
        )
    else:
        return False

