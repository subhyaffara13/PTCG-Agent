
def parse_credentials(netloc):
    username = password = None
    if '@' in netloc:
        prefix, netloc = netloc.rsplit('@', 1)
        if ':' not in prefix:
            username = prefix
        else:
            username, password = prefix.split(':', 1)
    if username:
        username = unquote(username)
    if password:
        password = unquote(password)
    return username, password, netloc

