
def _validate_backend_language(backend, language):
    """Throws error if backend and language are incompatible"""
    langs = _lang_lookup.get(backend.upper(), False)
    if not langs:
        raise ValueError("Unrecognized backend: " + backend)
    if language.upper() not in langs:
        raise ValueError(("Backend {} and language {} are "
                          "incompatible").format(backend, language))

