
def _sequence_repr_maker(
    left: str, right: str, base: type, limit: int = 8
) -> t.Callable[[DebugReprGenerator, t.Iterable[t.Any], bool], str]:
    def proxy(self: DebugReprGenerator, obj: t.Iterable[t.Any], recursive: bool) -> str:
        if recursive:
            return _add_subclass_info(f"{left}...{right}", obj, base)
        buf = [left]
        have_extended_section = False
        for idx, item in enumerate(obj):
            if idx:
                buf.append(", ")
            if idx == limit:
                buf.append('<span class="extended">')
                have_extended_section = True
            buf.append(self.repr(item))
        if have_extended_section:
            buf.append("</span>")
        buf.append(right)
        return _add_subclass_info("".join(buf), obj, base)

    return proxy

