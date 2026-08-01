
def load_cache_artifacts(serialized_artifacts: bytes) -> CacheInfo | None:
    """
    Hot loads cache artifacts that were previously serialized via
    save_cache_artifacts

    Example:

    # From a previous invocation
    artifacts = torch.compiler.save_cache_artifacts()

    torch.compiler.load_cache_artifacts(artifacts[0])
    """
    from ._cache import CacheArtifactManager, CacheInfo

    artifacts = CacheArtifactManager.deserialize(serialized_artifacts)
    if artifacts is not None:
        return CacheArtifactManager.populate_caches(artifacts)
    return None

