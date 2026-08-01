
def swizzle_mxfp4_convertops(blocks, scales, module, proj, target_device, triton_kernels_hub):
    """
    This transforms the weights obtained using `convert_gpt_oss.py` to load them into `Mxfp4GptOssExperts`.
    """
    PrecisionConfig, FlexCtx, InFlexData = (
        triton_kernels_hub.matmul_ogs.PrecisionConfig,
        triton_kernels_hub.matmul_ogs.FlexCtx,
        triton_kernels_hub.matmul_ogs.InFlexData,
    )

    local_experts = blocks.size(0)
    if (
        getattr(target_device, "type", target_device) == "cpu"
        and hasattr(torch, "accelerator")
        and torch.accelerator.current_accelerator() is not None
    ):
        target_device = torch.accelerator.current_accelerator().type

    blocks = blocks.to(target_device).contiguous()
    scales = scales.to(target_device).contiguous()

    if proj == "gate_up_proj":
        blocks = blocks.reshape(local_experts, module.intermediate_size * 2, -1)
    else:
        blocks = blocks.reshape(local_experts, -1, module.intermediate_size // 2)

    with on_device(target_device):
        triton_weight_tensor, weight_scale = swizzle_mxfp4(
            blocks.transpose(-2, -1), scales.transpose(-2, -1), triton_kernels_hub
        )
    # need to overwrite the shapes for the kernels
    if proj == "gate_up_proj":
        triton_weight_tensor.shape = torch.Size([local_experts, module.hidden_size, module.intermediate_size * 2])
    else:
        triton_weight_tensor.shape = torch.Size([local_experts, module.intermediate_size, module.hidden_size])

    # triton_weight_tensor is what needs to be passed in oai kernels. It stores the data, the shapes and any more objects. It's like a subtensor
    # Since the Experts module registers gate_up_proj and down_proj as nn.Parameters, we need to remove them so we can attach the Triton tensor
    if proj in module._parameters:
        # Remove the nn.Parameter registration so we can attach the Triton tensor
        del module._parameters[proj]
    setattr(module, proj, triton_weight_tensor)
    setattr(
        module,
        f"{proj}_precision_config",
        PrecisionConfig(weight_scale=weight_scale, flex_ctx=FlexCtx(rhs_data=InFlexData())),
    )

