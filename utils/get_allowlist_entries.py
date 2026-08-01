
def get_allowlist_entries(allowlist_file: str) -> Iterator[str]:
    def strip_comments(s: str) -> str:
        try:
            return s[: s.index("#")].strip()
        except ValueError:
            return s.strip()

    with open(allowlist_file) as f:
        for line in f:
            entry = strip_comments(line)
            if entry:
                yield entry

