
def _redact_responses_api_output_dict(output_items, redacted_str: str):
    """Helper to redact ResponsesAPIResponse output items in dict form."""
    for output_item in output_items:
        if not isinstance(output_item, dict):
            continue

        if "text" in output_item:
            output_item["text"] = redacted_str

        if isinstance(output_item.get("content"), list):
            for content_item in output_item["content"]:
                if isinstance(content_item, dict) and "text" in content_item:
                    content_item["text"] = redacted_str

        if output_item.get("type") == "reasoning" and isinstance(
            output_item.get("summary"), list
        ):
            for summary_item in output_item["summary"]:
                if isinstance(summary_item, dict) and "text" in summary_item:
                    summary_item["text"] = redacted_str

