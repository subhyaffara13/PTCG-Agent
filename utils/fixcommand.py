
def fixcommand(c):
    """Fix Qasm command names.

    Remove all of forbidden characters from command c, and
    replace 'def' with 'qdef'.
    """
    forbidden_characters = ['-']
    c = c.lower()
    for char in forbidden_characters:
        c = c.replace(char, '')
    if c == 'def':
        return 'qdef'
    return c

