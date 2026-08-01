
def _compile_replacement_helper(pattern, template):
    "Compiles a replacement template."
    # This function is called by the _regex module.

    # Have we seen this before?
    key = pattern.pattern, pattern.flags, template
    compiled = _replacement_cache.get(key)
    if compiled is not None:
        return compiled

    if len(_replacement_cache) >= _MAXREPCACHE:
        _replacement_cache.clear()

    is_unicode = isinstance(template, str)
    source = _Source(template)
    if is_unicode:
        def make_string(char_codes):
            return "".join(chr(c) for c in char_codes)
    else:
        def make_string(char_codes):
            return bytes(char_codes)

    compiled = []
    literal = []
    while True:
        ch = source.get()
        if not ch:
            break
        if ch == "\\":
            # '_compile_replacement' will return either an int group reference
            # or a string literal. It returns items (plural) in order to handle
            # a 2-character literal (an invalid escape sequence).
            is_group, items = _compile_replacement(source, pattern, is_unicode)
            if is_group:
                # It's a group, so first flush the literal.
                if literal:
                    compiled.append(make_string(literal))
                    literal = []
                compiled.extend(items)
            else:
                literal.extend(items)
        else:
            literal.append(ord(ch))

    # Flush the literal.
    if literal:
        compiled.append(make_string(literal))

    _replacement_cache[key] = compiled

    return compiled

