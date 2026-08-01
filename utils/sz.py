
def sz(s: bytes, o: int) -> bytes:
    return s[o : s.index(b"\0", o)]

