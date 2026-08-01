
def get_cache_key() -> str | None:
    # TODO: info versions of these logs that log only once
    if torch.compiler.config.force_disable_caches:
        warn_once(
            "dynamo_pgo force disabled by torch.compiler.config.force_disable_caches"
        )
        return None

    # NB: We namespace the cache keys so that only user-specified job id
    # can alias with each other.
    if (r := torch.compiler.config.job_id) is not None:
        if r.startswith("mast:"):
            raise ReservedWorkflowIdUserError(
                "torch.compiler.config.job_id with prefix 'mast:' is reserved for "
                "automatically generated job id associated with a specific MAST job "
                "name and version."
            )
        return format_cache_key(r)

    if (name_version := torch._utils_internal.get_mast_job_name_version()) is not None:
        mast_job_name, mast_job_version = name_version
        return format_cache_key(f"mast:{mast_job_name}:{mast_job_version}")

    return None


def get_cache_key(
    module: ir.Module,
    devices: np.ndarray,
    compile_options,
    backend,
    ignore_callbacks: cache_key.IgnoreCallbacks = cache_key.IgnoreCallbacks.NO,
) -> str:
  return cache_key.get(
      module,
      devices,
      compile_options,
      backend,
      "zstandard" if zstandard is not None else "zlib",
      ignore_callbacks,
  )

