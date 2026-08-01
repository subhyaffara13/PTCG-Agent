
def get_fingerprint(path, additional_parts):
    '''Return fingerprint string for Code Climate issue document.'''
    m = hashlib.md5()
    parts = [path, 'Complexity'] + additional_parts
    key = '|'.join(parts)
    m.update(key.encode('utf-8'))
    return m.hexdigest()

