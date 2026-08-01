
def aot_eager_decomp_partition_crossref(
    gm: torch.fx.GraphModule, fake_tensor_inputs: list[torch.Tensor], **kwargs: Any
) -> Callable[..., Any]:
    # if the config is set, respect it, otherwise only test custom_ops.
    # custom_op bad metas always manifest as an error whereas aten will only sometimes.
    # by default, use the less noisy option
    config_val = (
        "custom_ops"
        if not functorch_config.fake_tensor_crossref
        else functorch_config.fake_tensor_crossref
    )
    with functorch_config.patch(fake_tensor_crossref=config_val):
        return aot_eager_decomp_partition(gm, fake_tensor_inputs, **kwargs)

