
def format_str_literal(s: str) -> bytes:
    utf8 = s.encode("utf-8", errors="surrogatepass")
    return format_int(len(utf8)) + utf8

