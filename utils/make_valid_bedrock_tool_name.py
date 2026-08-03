import copy

def make_valid_bedrock_tool_name(input_tool_name: str) -> str:
    """Normalize tool names to Bedrock pattern [a-zA-Z][a-zA-Z0-9_-]*."""

    def replace_invalid(char):
        if char.isalnum() or char in ("_", "-"):
            return char
        return "_"

    # If the string is empty, return a default valid identifier
    if input_tool_name is None or len(input_tool_name) == 0:
        return input_tool_name
    bedrock_tool_name = copy.copy(input_tool_name)
    # If it doesn't start with a letter, prepend 'a'
    if not bedrock_tool_name[0].isalpha():
        bedrock_tool_name = "a" + bedrock_tool_name

    # Replace any invalid characters with underscores
    valid_string = "".join(replace_invalid(char) for char in bedrock_tool_name)

    if input_tool_name != valid_string:
        # passed tool name was formatted to become valid
        # store it internally so we can use for the response
        litellm.bedrock_tool_name_mappings.set_cache(
            key=valid_string, value=input_tool_name
        )

    return valid_string

