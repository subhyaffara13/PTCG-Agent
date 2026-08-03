from typing import Any, Callable

def _aot_stage2b_fw_compile(
    fw_module: torch.fx.GraphModule,
    adjusted_flat_args: list[Any],
    maybe_subclass_meta: SubclassMeta | None,
    fw_metadata: ViewAndMutationMeta,
    num_fw_outs_saved_for_bw: int,
    aot_config: AOTConfig,
    # pyrefly: ignore [implicit-any]
) -> tuple[list[tuple[int, ...] | None] | None, Callable]:
    return _aot_stage2b_compile_forward_or_inference(
        fw_module,
        adjusted_flat_args,
        maybe_subclass_meta,
        fw_metadata,
        aot_config,
        is_inference=False,
        num_fw_outs_saved_for_bw=num_fw_outs_saved_for_bw,
    )

