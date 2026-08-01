
def bucket_all_reduce(
    gm: torch.fx.GraphModule,
    bucket_cap_mb_by_bucket_idx: Callable[[int], float] | None = None,
    mode: str | None = None,
) -> None:
    if bucket_cap_mb_by_bucket_idx is None:
        from torch._inductor.fx_passes.bucketing import (
            bucket_cap_mb_by_bucket_idx_default,  # pyrefly: ignore [missing-module-attribute]
        )

        bucket_cap_mb_by_bucket_idx = bucket_cap_mb_by_bucket_idx_default
    ar_buckets = bucket_all_reduce_by_mb(gm, bucket_cap_mb_by_bucket_idx)
    if len(ar_buckets) == 0:
        return
    for bucket in ar_buckets:
        merge_all_reduce_bucket(gm.graph, bucket, mode)

