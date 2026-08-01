
def usual_language_name(language):
    """Return the usual language name (one that may be found in _SCRIPT_EXTENSIONS above)"""
    language = language.lower()
    if language == "r":
        return "R"
    if language.startswith("c++"):
        return "c++"
    if language == "octave":
        return "matlab"
    if language in ["cs", "c#"]:
        return "csharp"
    if language in ["fs", "f#"]:
        return "fsharp"
    if language == "sas":
        return "SAS"
    return language

