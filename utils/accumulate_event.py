from typing import Any

def accumulate_event(
    *,
    event: AssistantStreamEvent,
    current_message_snapshot: Message | None,
) -> tuple[Message | None, list[MessageContentDelta]]:
    """Returns a tuple of message snapshot and newly created text message deltas"""
    if event.event == "thread.message.created":
        return event.data, []

    new_content: list[MessageContentDelta] = []

    if event.event != "thread.message.delta":
        return current_message_snapshot, []

    if not current_message_snapshot:
        raise RuntimeError("Encountered a message delta with no previous snapshot")

    data = event.data
    if data.delta.content:
        for content_delta in data.delta.content:
            try:
                block = current_message_snapshot.content[content_delta.index]
            except IndexError:
                current_message_snapshot.content.insert(
                    content_delta.index,
                    cast(
                        MessageContent,
                        construct_type(
                            # mypy doesn't allow Content for some reason
                            type_=cast(Any, MessageContent),
                            value=model_dump(content_delta, exclude_unset=True, warnings=False),
                        ),
                    ),
                )
                new_content.append(content_delta)
            else:
                merged = accumulate_delta(
                    cast(
                        "dict[object, object]",
                        model_dump(block, exclude_unset=True, warnings=False),
                    ),
                    cast(
                        "dict[object, object]",
                        model_dump(content_delta, exclude_unset=True, warnings=False),
                    ),
                )
                current_message_snapshot.content[content_delta.index] = cast(
                    MessageContent,
                    construct_type(
                        # mypy doesn't allow Content for some reason
                        type_=cast(Any, MessageContent),
                        value=merged,
                    ),
                )

    return current_message_snapshot, new_content

