
def ot_tag_to_script(tag):
    """Return the Unicode script code for the given OpenType script tag, or
    None for "DFLT" tag or if there is no Unicode script associated with it.
    Raises ValueError if the tag is invalid.
    """
    tag = tostr(tag).strip()
    if not tag or " " in tag or len(tag) > 4:
        raise ValueError("invalid OpenType tag: %r" % tag)

    if tag in OTTags.SCRIPT_ALIASES:
        tag = OTTags.SCRIPT_ALIASES[tag]

    while len(tag) != 4:
        tag += str(" ")  # pad with spaces

    if tag == OTTags.DEFAULT_SCRIPT:
        # it's unclear which Unicode script the "DFLT" OpenType tag maps to,
        # so here we return None
        return None

    if tag in OTTags.NEW_SCRIPT_TAGS_REVERSED:
        return OTTags.NEW_SCRIPT_TAGS_REVERSED[tag]

    if tag in OTTags.SCRIPT_EXCEPTIONS_REVERSED:
        return OTTags.SCRIPT_EXCEPTIONS_REVERSED[tag]

    # This side of the conversion is fully algorithmic

    # Any spaces at the end of the tag are replaced by repeating the last
    # letter. Eg 'nko ' -> 'Nkoo'.
    # Change first char to uppercase
    script_code = tag[0].upper() + tag[1]
    for i in range(2, 4):
        script_code += script_code[i - 1] if tag[i] == " " else tag[i]

    if script_code not in Scripts.NAMES:
        return None
    return script_code

