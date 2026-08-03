import functools
from typing import Any

def _handle_combo_kernel_per_subkernel_blocks(
    size_hints: dict[str, int],
    inductor_meta: dict[str, Any],
    triton_meta: dict[str, Any],
    filename: str | None = None,
    reduction_hint: bool = False,
    tile_hint: Any = None,
    min_elem_per_thread: int = 0,
) -> list[Config] | None:
    """
    Handle per-subkernel config generation for combo kernels.

    Each sub-kernel gets its own block sizes (XBLOCK_0, XBLOCK_1, etc.) generated
    using the same heuristics as standalone Triton kernels.

    Returns base configs that vary (num_warps, num_stages) with all blocks at
    heuristic defaults. Stores per-subkernel candidate configs in
    inductor_meta["combo_tuning_groups"] for sequential chained autotuning
    in CachingAutotuner._combo_sequential_autotune().

    Returns:
        List of configs if combo kernel with combo_grid_meta and per-subkernel
        blocks enabled, None otherwise.
    """
    combo_meta = inductor_meta.get("combo_grid_meta")
    if combo_meta is None or "heuristic_0" not in combo_meta:
        return None

    num_kernels = combo_meta["num_kernels"]
    inductor_meta_clean = {
        k: v for k, v in inductor_meta.items() if k != "combo_grid_meta"
    }

    combined_kwargs: dict[str, int] = {}
    all_num_warps: list[int] = []
    all_num_stages: list[int] = []
    unique_warp_stage_pairs: OrderedSet[tuple[int, int]] = OrderedSet()

    combo_tuning_groups: list[dict[str, Any]] = []

    for i in range(num_kernels):
        subkernel_heuristic = combo_meta[f"heuristic_{i}"]
        size_hints_i = combo_meta[f"size_hints_{i}"]

        if subkernel_heuristic == "pointwise":
            cfgs = pointwise(
                size_hints_i,
                triton_meta=triton_meta,
                tile_hint=TileHint.SQUARE
                if combo_meta[f"tile_hint_{i}"] == "TileHint.SQUARE"
                else TileHint.DEFAULT,
                filename=filename,
                min_elem_per_thread=min_elem_per_thread,
                inductor_meta=inductor_meta_clean,
                return_configs=True,
            )
            skip_rblock = False
        elif subkernel_heuristic == "reduction":
            cfgs = reduction(
                size_hints_i,
                reduction_hint=ReductionHint[combo_meta[f"reduction_hint_{i}"]],
                triton_meta=triton_meta,
                filename=filename,
                inductor_meta=inductor_meta_clean,
                return_configs=True,
            )
            skip_rblock = False
        elif subkernel_heuristic == "persistent_reduction":
            cfgs = persistent_reduction(
                size_hints_i,
                reduction_hint=ReductionHint[combo_meta[f"reduction_hint_{i}"]],
                triton_meta=triton_meta,
                filename=filename,
                inductor_meta=inductor_meta_clean,
                return_configs=True,
            )
            skip_rblock = True  # persistent reduction embeds RBLOCK in kernel body
        else:
            raise ValueError(f"Unknown heuristic: {subkernel_heuristic}")

        cfg = cfgs[0]
        for key, value in cfg.kwargs.items():
            if skip_rblock and key.startswith("R") and "BLOCK" in key:
                continue
            combined_kwargs[f"{key}_{i}"] = value

        all_num_warps.append(cfg.num_warps)
        all_num_stages.append(cfg.num_stages)
        for c in cfgs:
            unique_warp_stage_pairs.add((c.num_warps, c.num_stages))

        combo_tuning_groups.append(
            {
                "member_indices": [i],
                "configs": cfgs,
                "skip_rblock": skip_rblock,
                "size_hints": size_hints_i,
            }
        )

    unique_warp_stage_pairs.add((max(all_num_warps), max(all_num_stages)))

    # Largest sub-kernels tuned first — they dominate runtime and get most freedom
    combo_tuning_groups.sort(
        key=lambda g: -functools.reduce(operator.mul, g["size_hints"].values())
    )
    inductor_meta["combo_tuning_groups"] = combo_tuning_groups
    # Candidates for num_warps/num_stages re-tuning after block sizes are finalized
    inductor_meta["combo_warp_stage_candidates"] = list(unique_warp_stage_pairs)

    # Single base config: max warps/stages, all blocks at heuristic defaults.
    # Block sizes are tuned in _combo_sequential_autotune, then num_warps/num_stages
    # are re-tuned at the end with finalized block sizes.
    base_num_warps = max(all_num_warps)
    base_num_stages = max(all_num_stages)
    return [
        triton.Config(
            combined_kwargs,
            num_warps=base_num_warps,
            num_stages=base_num_stages,
        )
    ]

