
def format_cache_key(key: str) -> str:
    # NB: We always use global rank for keys, even though they are overkill
    # for local only cache
    rank = None
    if dist.is_available() and dist.is_initialized():
        rank = dist.get_rank()

    tag = torch.compiler.config.cache_key_tag
    return f"{key}:{rank}:{tag}"

