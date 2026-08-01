
def gzip_accepted(accept_encoding_header: str) -> bool:
    accept_encoding_header = accept_encoding_header or ''
    for accepted in accept_encoding_header.split(','):
        if accepted.split(';')[0].strip().lower() == 'gzip':
            return True
    return False

