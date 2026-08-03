from typing import Callable

def bucket_all_gather(
    gm: torch.fx.GraphModule,
    bucket_cap_mb_by_bucket_idx: Callable[[int], float] | None = None,
    mode: BucketMode | None = None,
) -> None:
    mode = mode or _default_bucket_mode()
    if bucket_cap_mb_by_bucket_idx is None:
        from torch._inductor.fx_passes.bucketing import (
            bucket_cap_mb_by_bucket_idx_default,  # pyrefly: ignore [missing-module-attribute]
        )

        bucket_cap_mb_by_bucket_idx = bucket_cap_mb_by_bucket_idx_default
    ag_buckets = bucket_all_gather_by_mb(gm, bucket_cap_mb_by_bucket_idx, None, mode)
    if len(ag_buckets) == 0:
        return
    merge_all_gather(gm, ag_buckets, mode)

