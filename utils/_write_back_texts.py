from typing import List

def _write_back_texts(
    guardrailed_texts: List[str],
    holders: List[_StringHolder],
) -> None:
    if len(guardrailed_texts) < len(holders):
        verbose_proxy_logger.warning(
            "BedrockPassthroughGuardrailHandler: guardrail returned %d texts for %d "
            "extracted fields; the unreturned fields keep their original text",
            len(guardrailed_texts),
            len(holders),
        )
    for idx, (container, key) in enumerate(holders):
        if idx >= len(guardrailed_texts):
            break
        container[key] = guardrailed_texts[idx]

