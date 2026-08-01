
def _default_bucket_mode() -> BucketMode:
    from torch._inductor import config

    return config.aten_distributed_optimizations.bucket_mode or "default"

