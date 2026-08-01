
def fuse_fx(gm: torch.fx.GraphModule, example_inputs) -> torch.fx.GraphModule:
    is_cpu = is_cpu_device(example_inputs)
    # pyre-fixme[16]: Module `torch._dynamo.utils` has no attribute `detect_fake_mode`
    fake_mode = detect_fake_mode(example_inputs)

    gm = sink_cat_after_pointwise(gm)
    if config.permute_fusion and not is_cpu:
        # For linear permute fusion, we need to check input info to identify
        # and perform proper permutation/transpose
        ShapeProp(gm, fake_mode=fake_mode).propagate(*example_inputs)
        with GraphTransformObserver(gm, "linear_permute_fusion"):
            gm = linear_permute_fusion(gm)
        with GraphTransformObserver(gm, "permute_linear_fusion"):
            gm = permute_linear_fusion(gm)
        with GraphTransformObserver(gm, "permute_matmul_fusion"):
            gm = permute_matmul_fusion(gm)

    # make sure the autograd is disabled.
    if torch.is_grad_enabled() or not is_cpu:
        return gm
    if config.freezing:
        with GraphTransformObserver(gm, "remove_identity"):
            gm = remove_identity(gm)
        with GraphTransformObserver(gm, "fuse_conv_bn"):
            gm = fuse_conv_bn(gm)
    return gm


def fuse_fx(
    model: torch.nn.Module,
    fuse_custom_config: FuseCustomConfig | dict[str, Any] | None = None,
    backend_config: BackendConfig | dict[str, Any] | None = None,
) -> GraphModule:
    r"""Fuse modules like conv+bn, conv+bn+relu etc, model must be in eval mode.
    Fusion rules are defined in torch.ao.quantization.fx.fusion_pattern.py

    Args:

        * `model` (torch.nn.Module): a torch.nn.Module model
        * `fuse_custom_config` (FuseCustomConfig): custom configurations for fuse_fx.
            See :class:`~torch.ao.quantization.fx.custom_config.FuseCustomConfig` for more details
    Example::

        from torch.ao.quantization import fuse_fx

        m = Model().eval()
        m = fuse_fx(m)

    """
    if fuse_custom_config is None:
        fuse_custom_config = FuseCustomConfig()

    if isinstance(fuse_custom_config, dict):
        warnings.warn(
            "Passing a fuse_custom_config_dict to fuse is deprecated and will not be supported "
            "in a future version. Please pass in a FuseCustomConfig instead.",
            FutureWarning,
            stacklevel=2,
        )
        fuse_custom_config = FuseCustomConfig.from_dict(fuse_custom_config)

    torch._C._log_api_usage_once("quantization_api.quantize_fx.fuse_fx")
    preserved_attr_names = fuse_custom_config.preserved_attributes
    preserved_attrs = {
        attr: getattr(model, attr)
        for attr in preserved_attr_names
        if hasattr(model, attr)
    }

    graph_module = torch.fx.symbolic_trace(model)
    _attach_meta_to_node_if_not_exist(graph_module)
    graph_module = _fuse_fx(graph_module, False, fuse_custom_config, backend_config)

    attach_preserved_attrs_to_model(graph_module, preserved_attrs)
    return graph_module

