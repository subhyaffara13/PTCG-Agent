from typing import List, Union

def _build_bedrock_tool_result_content_blocks(
    message: Union[ChatCompletionToolMessage, ChatCompletionFunctionMessage],
) -> tuple[List[BedrockToolResultContentBlock], bool]:
    # Optional OpenAI tool-message extension:
    # allow structured Bedrock search results on tool messages and map them
    # directly to toolResult.content[].searchResult for Converse API.
    #
    # If `search_results` is present, we intentionally prefer it over `content`
    # to avoid generating mixed text + searchResult blocks.
    search_results = message.get("search_results")
    if isinstance(search_results, list):
        tool_result_content_blocks: List[BedrockToolResultContentBlock] = []
        for result in search_results:
            if not isinstance(result, dict):
                continue
            tool_result_content_blocks.append(
                BedrockToolResultContentBlock(
                    searchResult=cast(SearchResultBlock, result)
                )
            )
        if tool_result_content_blocks:
            return tool_result_content_blocks, True

    message_content = message["content"]
    if isinstance(message_content, str):
        return [BedrockToolResultContentBlock(text=message_content)], False
    if isinstance(message_content, List):
        return _parse_bedrock_tool_result_content_list(message_content), False
    return [], False

