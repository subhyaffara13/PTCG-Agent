
def replace_with_quant_layers(
    model: nn.Module,
    quantization_config=None,
    modules_to_not_convert: list[str] | None = None,
) -> None:
    """Replace `nn.Linear` / `nn.Embedding` modules with `QuantizedLinear` / `QuantizedEmbedding`.

    Per-module bit widths come from `quantization_config.module_quant_configs`.
    `nn.Embedding` modules are only replaced when `quantize_embeddings` is True.
    Modules whose name matches an entry in `modules_to_not_convert` are skipped.
    """
    import re

    from ..quantizers.quantizers_utils import should_convert_module

    quantize_embeddings = quantization_config.quantize_embeddings
    num_bits = quantization_config.num_bits
    module_quant_configs = quantization_config.module_quant_configs or {}

    # Join all the per-module patterns into one regex, compiled once, so each module name needs a
    # single search instead of a loop over patterns. Each pattern is a named group `g0`, `g1`, ...;
    # whichever group matches identifies its override.
    overrides_by_group = {f"g{i}": override for i, override in enumerate(module_quant_configs.values())}
    matcher = (
        re.compile("|".join(f"(?P<g{i}>{pattern})" for i, pattern in enumerate(module_quant_configs)))
        if module_quant_configs
        else None
    )

    for name, module in list(model.named_modules()):
        if not should_convert_module(name, modules_to_not_convert):
            continue
        opts = {"num_bits": num_bits}
        if matcher is not None and (match := matcher.search(name)) is not None:
            override = next(overrides_by_group[g] for g, v in match.groupdict().items() if v is not None)
            opts = {"num_bits": num_bits, **override}
        if isinstance(module, nn.Embedding):
            if not quantize_embeddings:
                continue
            new_module = QuantizedEmbedding(
                num_embeddings=module.num_embeddings,
                embedding_dim=module.embedding_dim,
                embed_scale=getattr(module, "scalar_embed_scale", 1.0),
                output_dtype=module.weight.dtype,
                **opts,
            )
        elif isinstance(module, nn.Linear):
            new_module = QuantizedLinear(
                in_features=module.in_features,
                out_features=module.out_features,
                bias=module.bias is not None,
                **opts,
            )
        else:
            continue
        new_module.requires_grad_(False)
        model.set_submodule(name, new_module)
    return model

