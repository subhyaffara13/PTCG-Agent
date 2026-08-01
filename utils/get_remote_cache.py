
def get_remote_cache() -> RemoteCache[JsonDataTy] | None:
    from torch._inductor.remote_cache import create_cache

    if not should_use_remote_dynamo_pgo_cache():
        return None

    return create_cache(
        "dynamo-pgo",
        is_fbcode(),
        "FbRemoteDynamoPGOCache",
        "RemoteDynamoPGOCache",
    )

