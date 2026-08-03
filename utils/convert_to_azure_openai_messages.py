from typing import List

def convert_to_azure_openai_messages(
    messages: List[AllMessageValues],
) -> List[AllMessageValues]:
    for m in messages:
        if m["role"] == "assistant":
            function_call = m.get("function_call", None)
            if function_call is not None:
                m["function_call"] = _azure_tool_call_invoke_helper(function_call)

        if m["role"] == "user" and isinstance(m.get("content"), list):
            for content in m.get("content", []):
                if isinstance(content, dict) and content.get("type") == "image_url":
                    _azure_image_url_helper(content)  # type: ignore
    return messages

