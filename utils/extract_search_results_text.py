
def extract_search_results_text(search_results: object) -> str:
    """
    Extract model-visible text from OpenAI tool-message ``search_results``.

    Used by token estimators and TPM limiters so large search result payloads
    cannot bypass preflight checks via a small ``content`` field.

    Counts every string field forwarded on Bedrock ``SearchResultBlock``:
    ``source``, ``title``, ``content[].text``, and ``citations``.
    """
    if not isinstance(search_results, list):
        return ""
    texts = ""
    for result in search_results:
        if not isinstance(result, dict):
            continue
        for key in ("source", "title"):
            value = result.get(key)
            if isinstance(value, str):
                texts += value
        content = result.get("content")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict):
                    text = block.get("text")
                    if isinstance(text, str):
                        texts += text
        citations = result.get("citations")
        if citations is not None:
            texts += json.dumps(citations, separators=(",", ":"))
    return texts

