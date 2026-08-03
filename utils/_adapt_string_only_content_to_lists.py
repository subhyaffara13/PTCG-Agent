from typing import Dict, List

def _adapt_string_only_content_to_lists(messages: List[Dict]):
    new_messages = []

    for message in messages:
        role = message.get("role")
        content = message.get("content")

        new_content = []

        if isinstance(content, str):
            new_content.append({"type": "text", "text": content})

        elif isinstance(content, dict):
            new_content.append(content)

        elif isinstance(content, list):
            new_content_items = []
            for content_item in content:
                if isinstance(content_item, str):
                    new_content_items.append({"type": "text", "text": content_item})
                elif isinstance(content_item, dict):
                    new_content_items.append(content_item)
                else:
                    raise Exception(
                        "`content` can only contain strings or openai content dicts"
                    )

            new_content += new_content_items
        else:
            raise Exception("Content must be a string")

        new_messages.append({"role": role, "content": new_content})

    return new_messages

