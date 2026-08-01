
def _infer_language(backend):
    """For a given backend, return the top choice of language"""
    langs = _lang_lookup.get(backend.upper(), False)
    if not langs:
        raise ValueError("Unrecognized backend: " + backend)
    return langs[0]

