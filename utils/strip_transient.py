
def strip_transient(nb):
    """Strip transient values that shouldn't be stored in files.

    This should be called in *both* read and write.
    """
    nb.pop("orig_nbformat", None)
    nb.pop("orig_nbformat_minor", None)
    for ws in nb["worksheets"]:
        for cell in ws["cells"]:
            cell.get("metadata", {}).pop("trusted", None)
            # strip cell.trusted even though it shouldn't be used,
            # since it's where the transient value used to be stored.
            cell.pop("trusted", None)
    return nb


def strip_transient(nb):
    """Strip transient values that shouldn't be stored in files.

    This should be called in *both* read and write.
    """
    nb.metadata.pop("orig_nbformat", None)
    nb.metadata.pop("orig_nbformat_minor", None)
    nb.metadata.pop("signature", None)
    for cell in nb.cells:
        cell.metadata.pop("trusted", None)
    return nb

