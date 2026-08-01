
def match_entity(stream):
    """Returns first entity in stream or None if no entity exists

    Note: For Bleach purposes, entities must start with a "&" and end with a
    ";". This ignores ambiguous character entities that have no ";" at the end.

    :arg stream: the character stream

    :returns: the entity string without "&" or ";" if it's a valid character
        entity; ``None`` otherwise

    """
    # Nix the & at the beginning
    if stream[0] != "&":
        raise ValueError('Stream should begin with "&"')

    stream = stream[1:]

    stream = list(stream)
    possible_entity = ""
    end_characters = "<&=;" + string.whitespace

    # Handle number entities
    if stream and stream[0] == "#":
        possible_entity = "#"
        stream.pop(0)

        if stream and stream[0] in ("x", "X"):
            allowed = "0123456789abcdefABCDEF"
            possible_entity += stream.pop(0)
        else:
            allowed = "0123456789"

        # FIXME(willkg): Do we want to make sure these are valid number
        # entities? This doesn't do that currently.
        while stream and stream[0] not in end_characters:
            c = stream.pop(0)
            if c not in allowed:
                break
            possible_entity += c

        if possible_entity and stream and stream[0] == ";":
            return possible_entity
        return None

    # Handle character entities
    while stream and stream[0] not in end_characters:
        c = stream.pop(0)
        possible_entity += c
        if not ENTITIES_TRIE.has_keys_with_prefix(possible_entity):
            # If it's not a prefix, then it's not an entity and we're
            # out
            return None

    if possible_entity and stream and stream[0] == ";":
        return possible_entity

    return None

