
def _sort_bedrock_assistant_content_blocks(
    blocks: List[BedrockContentBlock],
) -> List[BedrockContentBlock]:
    """
    Sort assistant content blocks so that ``text`` blocks appear before
    ``toolUse`` blocks.

    Bedrock requires all ``text`` blocks to precede any ``toolUse`` blocks
    within an assistant message.  When the Responses API converts
    function_call items before message items, the resulting ``toolUse``
    blocks can end up before ``text`` blocks, causing Bedrock to reject
    the request with a 400 error because the ``toolUse`` → ``toolResult``
    pairing is broken by the intervening ``text`` block.

    Sort order (stable):
      0 - reasoningContent
      1 - text / image / document / video / other non-tool blocks
      2 - toolUse
    """

    def _sort_key(block: BedrockContentBlock) -> int:
        if "reasoningContent" in block:
            return 0
        if "toolUse" in block:
            return 2
        if "cachePoint" in block:
            # cachePoint blocks are paired with their preceding toolUse block.
            # Same key as toolUse so Python's stable sort keeps them together.
            return 2
        return 1

    return sorted(blocks, key=_sort_key)

