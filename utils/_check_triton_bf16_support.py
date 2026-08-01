
def _check_triton_bf16_support(graph: GraphLowering) -> None:
    def warn_and_skip(device: torch.device | None) -> Never:
        from torch._dynamo.exc import SkipFrame

        assert device is not None

        device_interface = get_interface_for_device(device.type)
        device_props = device_interface.get_device_properties(device)
        warnings.warn(
            f"{device_props.name} does not support bfloat16 compilation natively, skipping"
        )
        raise SkipFrame("BF16 is not supported")

    for node in itertools.chain(graph.graph_inputs.values(), graph.graph_outputs):
        if not isinstance(node, IRNode):
            continue
        device_type = get_device_type(node)
        if (
            not device_type
            or not is_gpu(device_type)
            or node.get_dtype() != torch.bfloat16
        ):
            continue
        # Print warning and skip frame if attempting to compile for bfloat16
        # on device without hardware support for dtype
        device_interface = get_interface_for_device(device_type)
        if device_interface.is_bf16_supported(including_emulation=False):
            return
        warn_and_skip(node.get_device())

