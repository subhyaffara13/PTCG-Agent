from typing import Any, List, Tuple

def _extract_converse_output_texts(
    content_blocks: List[Any],
) -> Tuple[List[str], List[_StringHolder]]:
    """
    Collect user-visible text from Bedrock Converse output content blocks.

    Covers ``text`` blocks plus the other content-bearing fields a model can
    emit -- ``toolUse.input``, ``reasoningContent.reasoningText.text`` and
    ``citationsContent.content[].text`` -- while leaving structural values such
    as reasoning signatures and citation sources untouched.
    """
    holders: List[_StringHolder] = []
    for block in content_blocks:
        if not isinstance(block, dict):
            continue
        _collect_block_text(block, holders)
        tool_use = block.get("toolUse")
        if isinstance(tool_use, dict):
            _collect_strings(tool_use.get("input"), holders)
        reasoning = block.get("reasoningContent")
        if isinstance(reasoning, dict):
            reasoning_text = reasoning.get("reasoningText")
            if isinstance(reasoning_text, dict):
                _collect_block_text(reasoning_text, holders)
        citations = block.get("citationsContent")
        if isinstance(citations, dict):
            for cited in citations.get("content") or []:
                if isinstance(cited, dict):
                    _collect_block_text(cited, holders)
    texts = [container[key] for container, key in holders]
    return texts, holders

