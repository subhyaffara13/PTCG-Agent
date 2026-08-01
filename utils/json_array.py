
def JSONArray(state, scan_once, array_hook=None,
              _w=WHITESPACE.match, _ws=WHITESPACE_STR):
    (s, end) = state
    values = []
    nextchar = s[end:end + 1]
    if nextchar in _ws:
        end = _w(s, end + 1).end()
        nextchar = s[end:end + 1]
    # Look-ahead for trivial empty array
    if nextchar == ']':
        if array_hook is not None:
            values = array_hook(values)
        return values, end + 1
    elif nextchar == '':
        raise JSONDecodeError("Expecting value or ']'", s, end)
    _append = values.append
    while True:
        value, end = scan_once(s, end)
        _append(value)
        nextchar = s[end:end + 1]
        if nextchar in _ws:
            end = _w(s, end + 1).end()
            nextchar = s[end:end + 1]
        end += 1
        if nextchar == ']':
            break
        elif nextchar != ',':
            raise JSONDecodeError("Expecting ',' delimiter or ']'", s, end - 1)

        try:
            if s[end] in _ws:
                end += 1
                if s[end] in _ws:
                    end = _w(s, end + 1).end()
        except IndexError:
            pass

        if s[end:end + 1] == ']':
            raise JSONDecodeError(
                "Illegal trailing comma before end of array",
                s, end - 1)

    if array_hook is not None:
        values = array_hook(values)
    return values, end

