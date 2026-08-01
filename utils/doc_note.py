
def doc_note(initialdoc, note):
    """
    Adds a Notes section to an existing docstring.

    """
    if initialdoc is None:
        return
    if note is None:
        return initialdoc

    notesplit = re.split(r'\n\s*?Notes\n\s*?-----', inspect.cleandoc(initialdoc))
    notedoc = f"\n\nNotes\n-----\n{inspect.cleandoc(note)}\n"

    return ''.join(notesplit[:1] + [notedoc] + notesplit[1:])

