
def sort_messages_preserving_file_order(
    messages: list[str], prev_messages: list[str]
) -> list[str]:
    """Sort messages so that the order of files is preserved.

    An update generates messages so that the files can be in a fairly
    arbitrary order.  Preserve the order of files to avoid messages
    getting reshuffled continuously.  If there are messages in
    additional files, sort them towards the end.
    """
    # Calculate file order from the previous messages
    n = 0
    order = {}
    for msg in prev_messages:
        fnam = extract_fnam_from_message(msg)
        if fnam and fnam not in order:
            order[fnam] = n
            n += 1

    # Related messages must be sorted as a group of successive lines
    groups = []
    i = 0
    while i < len(messages):
        msg = messages[i]
        maybe_fnam = extract_possible_fnam_from_message(msg)
        group = [msg]
        if maybe_fnam in order:
            # This looks like a file name. Collect all lines related to this message.
            while (
                i + 1 < len(messages)
                and extract_possible_fnam_from_message(messages[i + 1]) not in order
                and extract_fnam_from_message(messages[i + 1]) is None
                and not messages[i + 1].startswith("mypy: ")
            ):
                i += 1
                group.append(messages[i])
        groups.append((order.get(maybe_fnam, n), group))
        i += 1

    groups = sorted(groups, key=lambda g: g[0])
    result = []
    for key, group in groups:
        result.extend(group)
    return result

