
def is_jupyter_language(language):
    """Is this a jupyter language?"""
    for lang in _JUPYTER_LANGUAGES:
        if language.lower() == lang.lower():
            return True
    return False

