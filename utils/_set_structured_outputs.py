
def _set_structured_outputs(span: "Span", response_obj, msg_attrs, span_attrs):
    output_items = response_obj.get("output", [])
    for i, item in enumerate(output_items):
        prefix = f"{span_attrs.LLM_OUTPUT_MESSAGES}.{i}"
        if not hasattr(item, "type"):
            continue

        item_type = item.type
        if item_type == "reasoning" and hasattr(item, "summary"):
            for summary in item.summary:
                if hasattr(summary, "text"):
                    safe_set_attribute(
                        span,
                        f"{prefix}.{msg_attrs.MESSAGE_REASONING_SUMMARY}",
                        summary.text,
                    )
        elif item_type == "message" and hasattr(item, "content"):
            message_content = ""
            content_list = item.content
            if content_list and len(content_list) > 0:
                first_content = content_list[0]
                message_content = getattr(first_content, "text", "")
            message_role = getattr(item, "role", "assistant")
            safe_set_attribute(span, span_attrs.OUTPUT_VALUE, message_content)
            safe_set_attribute(
                span, f"{prefix}.{msg_attrs.MESSAGE_CONTENT}", message_content
            )
            safe_set_attribute(span, f"{prefix}.{msg_attrs.MESSAGE_ROLE}", message_role)

