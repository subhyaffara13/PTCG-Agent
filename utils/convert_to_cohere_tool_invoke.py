
def convert_to_cohere_tool_invoke(tool_calls: list) -> List[ToolCallObject]:
    """
    OpenAI tool invokes:
    {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_abc123",
          "type": "function",
          "function": {
            "name": "get_current_weather",
            "arguments": "{\n\"location\": \"Boston, MA\"\n}"
          }
        }
      ]
    },
    """

    """
    Cohere tool invokes:
    {
      "role": "CHATBOT",
      "tool_calls": [{"name": "get_weather", "parameters": {"location": "San Francisco, CA"}}]
    }
    """

    cohere_tool_invoke: List[ToolCallObject] = [
        {
            "name": get_attribute_or_key(
                get_attribute_or_key(tool, "function"), "name"
            ),
            "parameters": json.loads(
                get_attribute_or_key(
                    get_attribute_or_key(tool, "function"), "arguments"
                )
            ),
        }
        for tool in tool_calls
        if get_attribute_or_key(tool, "type") == "function"
    ]

    return cohere_tool_invoke

