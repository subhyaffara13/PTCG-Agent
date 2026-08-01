
def parse_numeric_escape(source, info, ch, in_set):
    "Parses a numeric escape sequence."
    if in_set or ch == "0":
        # Octal escape sequence, max 3 digits.
        return parse_octal_escape(source, info, [ch], in_set)

    # At least 1 digit, so either octal escape or group.
    digits = ch
    saved_pos = source.pos
    ch = source.get()
    if ch in DIGITS:
        # At least 2 digits, so either octal escape or group.
        digits += ch
        saved_pos = source.pos
        ch = source.get()
        if is_octal(digits) and ch in OCT_DIGITS:
            # 3 octal digits, so octal escape sequence.
            encoding = info.flags & _ALL_ENCODINGS
            if encoding == ASCII or encoding == LOCALE:
                octal_mask = 0xFF
            else:
                octal_mask = 0x1FF

            value = int(digits + ch, 8) & octal_mask
            return make_character(info, value)

    # Group reference.
    source.pos = saved_pos
    if info.is_open_group(digits):
        raise error("cannot refer to an open group", source.string, source.pos)

    return make_ref_group(info, digits, source.pos)

