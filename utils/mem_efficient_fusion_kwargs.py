from typing import Any

def mem_efficient_fusion_kwargs(use_decomps: bool) -> dict[str, Any]:
    from functorch.compile import (
        default_decompositions,
        min_cut_rematerialization_partition,
        ts_compile,
    )

    kwargs = {
        # these are taken from memory_efficient_fusion()
        "fw_compiler": ts_compile,
        "bw_compiler": ts_compile,
        "partition_fn": min_cut_rematerialization_partition,
    }

    if use_decomps:
        # pyrefly: ignore [bad-typed-dict-key]
        kwargs["decompositions"] = default_decompositions

    return kwargs

