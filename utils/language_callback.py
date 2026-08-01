
def language_callback(lexer, match):
    """Parse the content of a $-string using a lexer

    The lexer is chosen looking for a nearby LANGUAGE or assumed as
    plpgsql if inside a DO statement and no LANGUAGE has been found.
    """
    lx = None
    m = language_re.match(lexer.text[match.end():match.end()+100])
    if m is not None:
        lx = lexer._get_lexer(m.group(1))
    else:
        m = list(language_re.finditer(
            lexer.text[max(0, match.start()-100):match.start()]))
        if m:
            lx = lexer._get_lexer(m[-1].group(1))
        else:
            m = list(do_re.finditer(
                lexer.text[max(0, match.start()-25):match.start()]))
            if m:
                lx = lexer._get_lexer('plpgsql')

    # 1 = $, 2 = delimiter, 3 = $
    yield (match.start(1), String, match.group(1))
    yield (match.start(2), String.Delimiter, match.group(2))
    yield (match.start(3), String, match.group(3))
    # 4 = string contents
    if lx:
        yield from lx.get_tokens_unprocessed(match.group(4))
    else:
        yield (match.start(4), String, match.group(4))
    # 5 = $, 6 = delimiter, 7 = $
    yield (match.start(5), String, match.group(5))
    yield (match.start(6), String.Delimiter, match.group(6))
    yield (match.start(7), String, match.group(7))

