
def fix_native_line_number(message: str, fnam: str, delta: int) -> str:
    """Update code locations in test case output to point to the .test file.

    The description of the test case is written to native.py, and line numbers
    in test case output often are relative to native.py. This translates the
    line numbers to be relative to the .test file that contains the test case
    description, and also updates the file name to the .test file name.

    Args:
        message: message to update
        fnam: path of the .test file
        delta: line number of the beginning of the test case in the .test file

    Returns updated message (or original message if we couldn't find anything).
    """
    fnam = os.path.basename(fnam)
    message = re.sub(
        r"native\.py:([0-9]+):", lambda m: "%s:%d:" % (fnam, int(m.group(1)) + delta), message
    )
    message = re.sub(
        r'"native.py", line ([0-9]+),',
        lambda m: '"%s", line %d,' % (fnam, int(m.group(1)) + delta),
        message,
    )
    return message

