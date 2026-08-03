import json
from typing import List

def stringify_json_tool_call_content(messages: List) -> List:
    """

    - Check 'content' in tool role -> convert to dict (if not) -> stringify

    Done for azure_ai/cohere calls to handle results of a tool call
    """

    for m in messages:
        if m["role"] == "tool" and isinstance(m["content"], str):
            # check if content is a valid json object
            try:
                json.loads(m["content"])
            except json.JSONDecodeError:
                m["content"] = json.dumps({"result": m["content"]})

    return messages

