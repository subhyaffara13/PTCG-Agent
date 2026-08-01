
def _is_eol_token(token):
    return token[0] in NEWLINE or token[4][token[3][1]:].lstrip() == '\\\n'

