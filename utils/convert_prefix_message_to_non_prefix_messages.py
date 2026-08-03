from typing import List

def convert_prefix_message_to_non_prefix_messages(
    messages: List[AllMessageValues],
) -> List[AllMessageValues]:
    """
    For models that don't support {prefix: true} in messages, we need to convert the prefix message to a non-prefix message.

    Use prompt:

    {"role": "assistant", "content": "value", "prefix": true} -> [
        {
            "role": "system",
            "content": "You are a helpful assistant. You are given a message and you need to respond to it. You are also given a generated content. You need to respond to the message in continuation of the generated content. Do not repeat the same content. Your response should be in continuation of this text: ",
        },
        {
            "role": "assistant",
            "content": message["content"],
        },
    ]

    do this in place
    """
    new_messages: List[AllMessageValues] = []
    for message in messages:
        if message.get("prefix"):
            new_messages.append(
                {
                    "role": "system",
                    "content": "You are a helpful assistant. You are given a message and you need to respond to it. You are also given a generated content. You need to respond to the message in continuation of the generated content. Do not repeat the same content. Your response should be in continuation of this text: ",
                }
            )
            new_messages.append(
                {**{k: v for k, v in message.items() if k != "prefix"}}  # type: ignore
            )
        else:
            new_messages.append(message)
    return new_messages

