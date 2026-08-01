
def _redact_responses_api_output(output_items):
    """Helper to redact ResponsesAPIResponse output items."""
    for output_item in output_items:
        if hasattr(output_item, "text"):
            output_item.text = "redacted-by-litellm"

        if hasattr(output_item, "content") and isinstance(output_item.content, list):
            for content_part in output_item.content:
                if hasattr(content_part, "text"):
                    content_part.text = "redacted-by-litellm"

        # Redact reasoning items in output array
        if hasattr(output_item, "type") and output_item.type == "reasoning":
            if hasattr(output_item, "summary") and isinstance(
                output_item.summary, list
            ):
                for summary_item in output_item.summary:
                    if hasattr(summary_item, "text"):
                        summary_item.text = "redacted-by-litellm"

