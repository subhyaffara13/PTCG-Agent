
def set_main_and_cell_language(metadata, cells, ext, custom_cell_magics):
    """Set main language for the given collection of cells, and
    use magics for cells that use other languages"""
    main_language = default_language_from_metadata_and_ext(metadata, ext)

    if main_language is None:
        languages = {"python": 0.5}
        for cell in cells:
            if "language" in cell["metadata"]:
                language = usual_language_name(cell["metadata"]["language"])
                languages[language] = languages.get(language, 0.0) + 1

        main_language = max(languages, key=languages.get)

    # save main language when no kernel is set
    if "language" not in metadata.get("kernelspec", {}) and cells:
        metadata.setdefault("jupytext", {})["main_language"] = main_language

    # Remove 'language' meta data and add a magic if not main language
    for cell in cells:
        if "language" in cell["metadata"]:
            language = cell["metadata"]["language"]
            if language == main_language:
                cell["metadata"].pop("language")
                continue

            if usual_language_name(language) == main_language:
                continue

            if language in _JUPYTER_LANGUAGES or language in custom_cell_magics:
                cell["metadata"].pop("language")
                magic = "%%" if main_language != "csharp" else "#!"
                if "magic_args" in cell["metadata"]:
                    magic_args = cell["metadata"].pop("magic_args")
                    cell["source"] = f"{magic}{language} {magic_args}\n" + cell["source"]
                else:
                    cell["source"] = f"{magic}{language}\n" + cell["source"]

