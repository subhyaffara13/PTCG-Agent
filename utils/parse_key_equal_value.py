
def parse_key_equal_value(text):
    """Parse a string of the form 'key1=value1 key2=value2'"""
    # Empty metadata?
    text = text.strip()
    if not text:
        return {}

    last_space_pos = text.rfind(" ")

    # Just an identifier?
    if not text.startswith("--") and is_identifier(text[last_space_pos + 1 :]):
        key = text[last_space_pos + 1 :]
        value = None
        result = {key: value}
        if last_space_pos > 0:
            result.update(parse_key_equal_value(text[:last_space_pos]))
        return result

    # Iterate on the '=' signs, starting from the right
    equal_sign_pos = None
    while True:
        equal_sign_pos = text.rfind("=", None, equal_sign_pos)
        if equal_sign_pos < 0:
            return incorrectly_encoded_metadata(text)

        # Do we have an identifier on the left of the equal sign?
        prev_whitespace = text[:equal_sign_pos].rstrip().rfind(" ")
        key = text[prev_whitespace + 1 : equal_sign_pos].strip()
        if not is_valid_metadata_key(key):
            continue

        try:
            value = relax_json_loads(text[equal_sign_pos + 1 :])
        except (ValueError, SyntaxError):
            # try with a longer expression
            continue

        # Combine with remaining metadata
        metadata = parse_key_equal_value(text[:prev_whitespace]) if prev_whitespace > 0 else {}

        # Append our value
        metadata[key] = value

        # And return
        return metadata

