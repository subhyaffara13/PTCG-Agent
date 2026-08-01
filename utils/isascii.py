
def isascii(s):
    try:
        s.encode('ascii')
    except UnicodeError:
        return False
    return True

