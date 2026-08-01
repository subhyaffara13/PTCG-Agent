
def _rename_duplicate_bedrock_document_names(
    contents: List[BedrockMessageBlock],
) -> List[BedrockMessageBlock]:
    """
    Rename duplicate document names across all messages in a Bedrock request.

    Document names are derived from a content hash, so the same file appearing
    in multiple conversation turns produces identical names and Bedrock rejects
    the request with "Messages can not contain duplicate document names".  The
    first occurrence keeps its original name so prompt-cache prefixes stay
    stable; later occurrences get a deterministic positional suffix
    (``_2``, ``_3``, ...), bumped further if the suffixed name already
    belongs to another document (e.g. an organic name ending in ``_2``).
    """
    used_names: Set[str] = set()
    for message in contents:
        for block in message.get("content") or []:
            document = block.get("document")
            if isinstance(document, dict) and document.get("name"):
                used_names.add(document["name"])

    name_counts: Dict[str, int] = {}
    for message in contents:
        for block in message.get("content") or []:
            document = block.get("document")
            if not isinstance(document, dict):
                continue
            name = document.get("name")
            if not name:
                continue
            count = name_counts.get(name, 0) + 1
            name_counts[name] = count
            if count > 1:
                suffix = count
                new_name = f"{name}_{suffix}"
                while new_name in used_names:
                    suffix += 1
                    new_name = f"{name}_{suffix}"
                used_names.add(new_name)
                document["name"] = new_name
    return contents

