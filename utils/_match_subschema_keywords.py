
def _match_subschema_keywords(value):
    for keyword in _SUBSCHEMAS_KEYWORDS:
        if keyword in value:
            yield keyword, value

