
def ensure_slash(s):
    if not s.endswith('/'):
        return s + '/'
    return s

