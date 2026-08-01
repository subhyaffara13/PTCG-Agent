
def save_cache_artifacts() -> tuple[bytes, CacheInfo] | None:
    """
    Serializes all the cache artifacts that were created during the compilation

    Example:

    - Execute torch.compile
    - Call torch.compiler.save_cache_artifacts()
    """
    from ._cache import CacheArtifactManager

    if torch._dynamo.config.caching_precompile:
        from torch._dynamo.precompile_context import PrecompileContext

        PrecompileContext.save_to_dynamo_cache()

    return CacheArtifactManager.serialize()

