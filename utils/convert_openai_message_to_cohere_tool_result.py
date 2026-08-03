import json
from typing import List, Union

def convert_openai_message_to_cohere_tool_result(
    message: Union[ChatCompletionToolMessage, ChatCompletionFunctionMessage],
    tool_calls: List,
) -> ToolResultObject:
    """
    OpenAI message with a tool result looks like:
    {
            "tool_call_id": "tool_1",
            "role": "tool",
            "content": {"location": "San Francisco, CA", "unit": "fahrenheit", "temperature": "72"},
    },
    """
    """
    OpenAI message with a function call looks like:
    {
        "role": "function",
        "name": "get_current_weather",
        "content": "function result goes here",
    }
    """

    """
    Cohere tool_results look like:
    {
       "call": {
           "name": "query_daily_sales_report",
           "parameters": {
               "day": "2023-09-29"
           },
       },
       "outputs": [
           {
               "date": "2023-09-29",
               "summary": "Total Sales Amount: 10000, Total Units Sold: 250"
           }
       ]
   },
    """

    content_str: str = ""
    if isinstance(message["content"], str):
        content_str = message["content"]
    elif isinstance(message["content"], List):
        content_list = message["content"]
        for content in content_list:
            if content["type"] == "text":
                content_str += content["text"]
    if len(content_str) > 0:
        try:
            content = json.loads(content_str)
        except json.JSONDecodeError:
            content = {"result": content_str}
    else:
        content = {}
    name = ""
    arguments = {}
    # Recover name from last message with tool calls
    if len(tool_calls) > 0:
        tools = tool_calls
        msg_tool_call_id = message.get("tool_call_id", None)
        for tool in tools:
            prev_tool_call_id = tool.get("id", None)
            if (
                msg_tool_call_id
                and prev_tool_call_id
                and msg_tool_call_id == prev_tool_call_id
            ):
                name = tool.get("function", {}).get("name", "")
                arguments_str = tool.get("function", {}).get("arguments", "")
                if arguments_str is not None and len(arguments_str) > 0:
                    arguments = json.loads(arguments_str)

    if message["role"] == "function":
        function_message: ChatCompletionFunctionMessage = message
        name = function_message["name"]
        cohere_tool_result: ToolResultObject = {
            "call": CallObject(name=name, parameters=arguments),
            "outputs": [content],
        }
        return cohere_tool_result
    else:
        # We can't determine from openai message format whether it's a successful or
        # error call result so default to the successful result template

        cohere_tool_result = {
            "call": CallObject(name=name, parameters=arguments),
            "outputs": [content],
        }
        return cohere_tool_result

