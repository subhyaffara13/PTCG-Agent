
def text_to_metadata(text, allow_title=False):
    """Parse the language/cell title and associated metadata"""
    # Parse the language or cell title = everything before the last blank space before { or =
    text = text.strip()
    first_curly_bracket = text.find("{")
    first_equal_sign = text.find("=")

    if first_curly_bracket < 0 or (0 <= first_equal_sign < first_curly_bracket):
        # this is a key=value metadata line
        # case one = the options may be preceded with a language
        if not allow_title:
            if is_jupyter_language(text):
                return text, {}
            if " " not in text:
                return "", parse_key_equal_value(text)
            language, options = text.split(" ", 1)
            if is_jupyter_language(language):
                return language, parse_key_equal_value(options)
            return "", parse_key_equal_value(text)

        # case two = a title may be before the options
        # we split the title into words
        if first_equal_sign >= 0:
            words = text[:first_equal_sign].split(" ")
            # last word is the key before the equal sign!
            while words and not words[-1]:
                words.pop()
            if words:
                words.pop()
        else:
            words = text.split(" ")

        # and we remove words on the right that are attributes (they start with '.')
        while words and (not words[-1].strip() or words[-1].startswith(".")):
            words.pop()

        title = " ".join(words)
        return title, parse_key_equal_value(text[len(title) :])

    # json metadata line
    return (
        text[:first_curly_bracket].strip(),
        relax_json_loads(text[first_curly_bracket:], catch=True),
    )

