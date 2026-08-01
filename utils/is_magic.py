
def is_magic(line, language, global_escape_flag=True, explicitly_code=False):
    """Is the current line a (possibly escaped) Jupyter magic, and should it be commented?"""
    language = usual_language_name(language)
    if language in ["octave", "matlab", "sas", "logtalk"] or language not in _SCRIPT_LANGUAGES:
        return False
    if _MAGIC_FORCE_ESC_RE[language].match(line):
        return True
    if not global_escape_flag or _MAGIC_NOT_ESC_RE[language].match(line):
        return False
    if _MAGIC_RE[language].match(line):
        return True
    if language != "python":
        return False
    if _PYTHON_HELP_OR_BASH_CMD.match(line):
        return True
    if _PYTHON_MAGIC_ASSIGN.match(line):
        return True
    if explicitly_code and _IPYTHON_MAGIC_HELP.match(line):
        return True
    return _PYTHON_MAGIC_CMD.match(line)

