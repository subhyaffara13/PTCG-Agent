
def _writeNote(glyphObject: Any, element: ElementType, validate: bool) -> None:
    note = getattr(glyphObject, "note", None)
    if validate and not isinstance(note, str):
        raise GlifLibError("note attribute must be str")
    if isinstance(note, str):
        note = note.strip()
        note = "\n" + note + "\n"
        etree.SubElement(element, "note").text = note

