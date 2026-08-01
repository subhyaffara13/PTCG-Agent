
def _readNote(glyphObject: Optional[Any], note: ElementType) -> None:
    if note.text is None:
        return
    lines = note.text.split("\n")
    note = "\n".join(line.strip() for line in lines if line.strip())
    _relaxedSetattr(glyphObject, "note", note)

