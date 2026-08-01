
def adapt_messages_to_bytez_standard(messages: List[Dict]):
    messages = _adapt_string_only_content_to_lists(messages)

    new_messages = []

    for message in messages:
        role = message["role"]
        content: list = message["content"]

        new_content = []

        for content_item in content:
            type: Union[str, None] = content_item.get("type")

            if not type:
                raise Exception("Prop `type` is not a string")

            content_item_map = open_ai_to_bytez_content_item_map[type]

            if not content_item_map:
                raise Exception(f"Prop `{type}` is not supported")

            new_type = content_item_map["type"]

            value_name = content_item_map["value_name"]

            value: Union[str, None] = content_item.get(value_name)

            if not value:
                raise Exception(f"Prop `{value_name}` is not a string")

            new_content.append({"type": new_type, value_name: value})

        new_messages.append({"role": role, "content": new_content})

    return new_messages

