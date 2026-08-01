
def add_cache_point_tool_block(
    tool: dict, model: Optional[str] = None
) -> Optional[BedrockToolBlock]:
    from litellm.llms.bedrock.common_utils import is_claude_4_5_on_bedrock

    cache_control = tool.get("cache_control", None)
    if cache_control is not None:
        cache_point = cache_control.get("type", "ephemeral")
        if cache_point == "ephemeral":
            cache_point_block: CachePointBlock = {"type": "default"}
            if isinstance(cache_control, dict) and "ttl" in cache_control:
                ttl = cache_control["ttl"]
                if (
                    ttl in ["5m", "1h"]
                    and model is not None
                    and is_claude_4_5_on_bedrock(model)
                ):
                    cache_point_block["ttl"] = ttl
            return {"cachePoint": cache_point_block}
    return None

