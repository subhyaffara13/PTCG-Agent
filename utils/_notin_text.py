
def _notin_text(term: str, text: str, verbose: int = 0) -> Iterator[str]:
    index = text.find(term)
    head = text[:index]
    tail = text[index + len(term) :]
    correct_text = head + tail
    diff = _diff_text(text, correct_text, dummy_highlighter, verbose)
    yield f"{saferepr(term, maxsize=42)} is contained here:"
    for line in diff:
        if line.startswith("Skipping"):
            continue
        if line.startswith("- "):
            continue
        if line.startswith("+ "):
            yield "  " + line[2:]
        else:
            yield line

