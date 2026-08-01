
def _validate_dduf_entry_name(entry_name: str) -> str:
    if "." + entry_name.split(".")[-1] not in DDUF_ALLOWED_ENTRIES:
        raise DDUFInvalidEntryNameError(f"File type not allowed: {entry_name}")
    if "\\" in entry_name:
        raise DDUFInvalidEntryNameError(f"Entry names must use UNIX separators ('/'). Got {entry_name}.")
    entry_name = entry_name.strip("/")
    if entry_name.count("/") > 1:
        raise DDUFInvalidEntryNameError(f"DDUF only supports 1 level of directory. Got {entry_name}.")
    return entry_name

