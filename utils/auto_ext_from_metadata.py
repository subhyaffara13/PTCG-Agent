
def auto_ext_from_metadata(metadata):
    """Script extension from notebook metadata"""
    auto_ext = metadata.get("language_info", {}).get("file_extension")

    # Sage notebooks have ".py" as the associated extension in "language_info",
    # so we change it to ".sage" in that case, see #727
    if auto_ext == ".py" and metadata.get("kernelspec", {}).get("language") == "sage":
        auto_ext = ".sage"

    if auto_ext is None:
        language = metadata.get("kernelspec", {}).get("language") or metadata.get("jupytext", {}).get("main_language")
        if language:
            for ext in _SCRIPT_EXTENSIONS:
                if same_language(language, _SCRIPT_EXTENSIONS[ext]["language"]):
                    auto_ext = ext
                    break

    if auto_ext == ".r":
        return ".R"

    if auto_ext == ".fs":
        return ".fsx"

    if auto_ext == ".resource":
        return ".robot"

    # Handle ROOT C++ notebooks
    # https://tinyurl.com/root-cpp-notebook-doc
    if auto_ext == ".C":
        return ".cpp"

    return auto_ext

