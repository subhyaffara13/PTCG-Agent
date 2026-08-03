from typing import List, Union

def _transform_prompt(
    messages: Union[List[AllMessageValues], List[OpenAITextCompletionUserMessage]],
) -> AllPromptValues:
    if len(messages) == 1:  # base case
        message_content = messages[0].get("content")
        if (
            message_content
            and isinstance(message_content, list)
            and is_tokens_or_list_of_tokens(message_content)
        ):
            openai_prompt: AllPromptValues = cast(AllPromptValues, message_content)
        else:
            openai_prompt = ""
            content = convert_content_list_to_str(cast(AllMessageValues, messages[0]))
            openai_prompt += content
    else:
        prompt_str_list: List[str] = []
        for m in messages:
            try:  # expect list of int/list of list of int to be a 1 message array only.
                content = convert_content_list_to_str(cast(AllMessageValues, m))
                prompt_str_list.append(content)
            except Exception as e:
                raise e
        openai_prompt = prompt_str_list
    return openai_prompt

