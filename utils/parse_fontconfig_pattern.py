
def parse_fontconfig_pattern(pattern):
    """
    Parse a fontconfig *pattern* into a dict that can initialize a
    `.font_manager.FontProperties` object.
    """
    parser = _make_fontconfig_parser()
    try:
        parse = parser.parse_string(pattern)
    except ParseException as err:
        # explain becomes a plain method on pyparsing 3 (err.explain(0)).
        raise ValueError("\n" + ParseException.explain(err, 0)) from None
    parser.reset_cache()
    props = {}
    if "families" in parse:
        props["family"] = [*map(_family_unescape, parse["families"])]
    if "sizes" in parse:
        props["size"] = [*parse["sizes"]]
    for prop in parse.get("properties", []):
        if len(prop) == 1:
            prop = _CONSTANTS[prop[0]]
        k, *v = prop
        props.setdefault(k, []).extend(map(_value_unescape, v))
    return props

