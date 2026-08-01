
def _aot_stage2b_inference_compile(
    fw_module: torch.fx.GraphModule,
    updated_flat_args: list[Any],
    maybe_subclass_meta: SubclassMeta | None,
    fw_metadata: ViewAndMutationMeta,
    aot_config: AOTConfig,
    # pyrefly: ignore [implicit-any]
) -> Callable:
    return _aot_stage2b_compile_forward_or_inference(
        fw_module,
        updated_flat_args,  # type: ignore[arg-type]
        maybe_subclass_meta,
        fw_metadata,
        aot_config,
        is_inference=True,
    )[1]

