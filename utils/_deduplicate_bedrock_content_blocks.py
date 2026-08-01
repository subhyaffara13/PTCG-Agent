
def _deduplicate_bedrock_content_blocks(
    blocks: List[BedrockContentBlock],
    block_key: str,
    id_key: str = "toolUseId",
) -> List[BedrockContentBlock]:
    """
    Remove duplicate content blocks that share the same ID under ``block_key``.

    Bedrock requires all toolResult and toolUse IDs within a single message to
    be unique.  When merging consecutive messages, duplicates can occur if the
    same tool_call_id appears multiple times in conversation history.

    When duplicates exist, the first occurrence is retained and subsequent ones
    are discarded.  A warning is logged for every dropped block so that
    upstream duplication bugs remain visible.

    Blocks that do not contain ``block_key`` (e.g., cachePoint, text) are
    always preserved.

    Args:
        blocks: The list of Bedrock content blocks to deduplicate.
        block_key: The dict key to inspect (e.g. ``"toolResult"`` or ``"toolUse"``).
        id_key: The nested key that holds the unique ID (default ``"toolUseId"``).
    """
    seen_ids: Set[str] = set()
    deduplicated: List[BedrockContentBlock] = []
    for block in blocks:
        keyed = block.get(block_key)
        if keyed is not None and isinstance(keyed, dict):
            block_id = keyed.get(id_key)
            if block_id:
                if block_id in seen_ids:
                    verbose_logger.warning(
                        "Bedrock Converse: dropping duplicate %s block with "
                        "%s=%s. This may indicate duplicate tool messages in "
                        "conversation history.",
                        block_key,
                        id_key,
                        block_id,
                    )
                    continue
                seen_ids.add(block_id)
        deduplicated.append(block)
    return deduplicated

