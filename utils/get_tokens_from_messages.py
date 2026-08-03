from typing import List

def get_tokens_from_messages(messages: List[dict]):
    total = 0

    for message in messages:
        content: List[dict] = message["content"]

        for content_item in content:
            type = content_item["type"]
            if type == "text":
                value: str = content_item["text"]
                words = value.split(" ")
                total += len(words)
                continue
            # we'll count media as single tokens for now
            total += 1

    return total

