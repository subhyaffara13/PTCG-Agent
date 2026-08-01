
def escape_string(s: str, escape_sequences: Collection[str] = _basic_escapes) -> str:
    s = decode(s)

    res = []
    start = 0

    def flush(inc: int = 1) -> int:
        if start != i:
            res.append(s[start:i])

        return i + inc

    found_sequences = {seq for seq in escape_sequences if seq in s}

    i = 0
    while i < len(s):
        for seq in found_sequences:
            seq_len = len(seq)
            if s[i:].startswith(seq):
                start = flush(seq_len)
                res.append(_compact_escapes.get(seq) or _unicode_escape(seq))
                i += seq_len - 1  # fast-forward escape sequence
        i += 1

    flush()

    return "".join(res)

