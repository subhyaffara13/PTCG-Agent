
def call_delegate_proxy_torch_dispatch_mode(
    mode: ProxyTorchDispatchMode,
    lowered_module: AOTI_LOWERED_MODULE,  # type: ignore[valid-type]
    original_gm: torch.fx.GraphModule,
    weight_args: list[torch.Tensor],
    input_args: list[torch.Tensor],
):
    res = trace_aoti_call_delegate(
        mode, aoti_call_delegate, lowered_module, original_gm, weight_args, input_args
    )
    return res


def call_delegate_proxy_torch_dispatch_mode(mode, lowered_module, *args):
    res = trace_call_delegate(mode, executorch_call_delegate, lowered_module, *args)
    return res

