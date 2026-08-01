
def _get_all_bedrock_regions() -> List[str]:
    """Get all Bedrock regions, cached at module level."""
    global _BEDROCK_GLOBAL_REGIONS
    if _BEDROCK_GLOBAL_REGIONS is None:
        _BEDROCK_GLOBAL_REGIONS = AmazonBedrockGlobalConfig().get_all_regions()
    return _BEDROCK_GLOBAL_REGIONS

