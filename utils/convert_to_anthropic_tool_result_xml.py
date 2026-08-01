
def convert_to_anthropic_tool_result_xml(message: dict) -> str:
    """
    OpenAI message with a tool result looks like:
    {
        "tool_call_id": "tool_1",
        "role": "tool",
        "name": "get_current_weather",
        "content": "function result goes here",
    },
    """

    """
    Anthropic tool_results look like:

    [Successful results]
    <function_results>
    <result>
    <tool_name>get_current_weather</tool_name>
    <stdout>
    function result goes here
    </stdout>
    </result>
    </function_results>

    [Error results]
    <function_results>
    <error>
    error message goes here
    </error>
    </function_results>
    """
    name = message.get("name")
    content = message.get("content", "")
    content = content.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")

    # We can't determine from openai message format whether it's a successful or
    # error call result so default to the successful result template
    anthropic_tool_result = (
        "<function_results>\n"
        "<result>\n"
        f"<tool_name>{name}</tool_name>\n"
        "<stdout>\n"
        f"{content}\n"
        "</stdout>\n"
        "</result>\n"
        "</function_results>"
    )

    return anthropic_tool_result

