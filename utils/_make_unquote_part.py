import re

def _make_unquote_part(name: str, chars: str) -> t.Callable[[str], str]:
    """Create a function that unquotes all percent encoded characters except those
    given. This allows working with unquoted characters if possible while not changing
    the meaning of a given part of a URL.
    """
    choices = "|".join(f"{ord(c):02X}" for c in sorted(chars))
    pattern = re.compile(f"((?:%(?:{choices}))+)", re.I)

    def _unquote_partial(value: str) -> str:
        parts = iter(pattern.split(value))
        out = []

        for part in parts:
            out.append(unquote(part, "utf-8", "werkzeug.url_quote"))
            out.append(next(parts, ""))

        return "".join(out)

    _unquote_partial.__name__ = f"_unquote_{name}"
    return _unquote_partial

