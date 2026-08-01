
def _validate_metric_label_name_token(tok: str) -> None:
    """Raises ValueError if a parsed label name token is invalid. 
    
    UTF-8 names must be quoted.
    """
    if not tok:
        raise ValueError("invalid label name token " + tok)
    quoted = tok[0] == '"' and tok[-1] == '"'
    if not quoted or _legacy_validation:
        if not METRIC_LABEL_NAME_RE.match(tok):
            raise ValueError("invalid label name token " + tok)
        return
    try:
        tok.encode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("invalid label name token " + tok)

