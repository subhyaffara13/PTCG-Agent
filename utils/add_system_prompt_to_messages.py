from typing import Dict, List, Union

def add_system_prompt_to_messages(
    messages: List[AllMessageValues],
    system_prompt: str,
    merge_with_first_system: bool = False,
) -> List[AllMessageValues]:
    """
    Add a system prompt to the messages list.

    Args:
        messages: List of chat completion messages
        system_prompt: The system prompt content to add. If empty or None, returns messages unchanged.
        merge_with_first_system: If True and the first message is already a system message,
            prepends the new prompt to that message's content. If False, adds a new system
            message at the beginning.

    Returns:
        New list of messages with the system prompt added
    """
    if not system_prompt:
        return list(messages)

    if merge_with_first_system and messages and messages[0].get("role") == "system":
        first = dict(messages[0])
        existing_content = first.get("content", "")
        merged_content: Union[str, List[Dict[str, str]]]
        if isinstance(existing_content, str):
            merged_content = f"{system_prompt.strip()}\n\n{existing_content}"
        elif isinstance(existing_content, list):
            merged_content = [{"type": "text", "text": system_prompt.strip()}] + list(
                existing_content
            )
        else:
            merged_content = [{"type": "text", "text": system_prompt.strip()}]
        first["content"] = merged_content
        return [cast(AllMessageValues, first)] + list(messages[1:])

    system_message: AllMessageValues = {"role": "system", "content": system_prompt}
    return [system_message, *messages]

