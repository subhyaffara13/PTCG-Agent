
def get_extra_cache_key(sticky_key: str) -> str | None:
    if torch.compiler.config.force_disable_caches:
        warn_once(
            "dynamo_pgo force disabled by torch.compiler.config.force_disable_caches"
        )
        return None

    return format_cache_key(sticky_key)

