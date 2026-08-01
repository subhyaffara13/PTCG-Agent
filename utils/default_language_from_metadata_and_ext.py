
def default_language_from_metadata_and_ext(metadata, ext, pop_main_language=False):
    """Return the default language given the notebook metadata, and a file extension"""
    default_from_ext = _SCRIPT_EXTENSIONS.get(ext, {}).get("language")

    main_language = metadata.get("jupytext", {}).get("main_language")
    default_language = metadata.get("kernelspec", {}).get("language") or default_from_ext
    language = main_language or default_language

    if main_language is not None and main_language == default_language and pop_main_language:
        metadata["jupytext"].pop("main_language")

    if language is None or language in ["R", "sas"]:
        return language

    if language.startswith("C++"):
        return "c++"

    return language.lower().replace("#", "sharp")

