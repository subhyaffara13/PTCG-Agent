import re

def rmd_options_to_metadata(options, use_runtools=False):
    """Parse rmd options and return a metadata dictionary"""
    options = re.split(r"\s|,", options, maxsplit=1)
    # Special case Wolfram Language, which sadly has a space in the language
    # name.
    if options[0:2] == ["wolfram", "language"]:
        options[0:2] = ["wolfram language"]
    if len(options) == 1:
        language = options[0]
        chunk_options = []
    else:
        language, others = options
        language = language.rstrip(" ,")
        others = others.lstrip(" ,")
        chunk_options = parse_rmd_options(others)

    language = "R" if language == "r" else language
    metadata = {}
    for i, opt in enumerate(chunk_options):
        name, value = opt
        if i == 0 and name == "":
            metadata["name"] = value
            continue
        if update_metadata_from_rmd_options(name, value, metadata, use_runtools=use_runtools):
            continue
        try:
            metadata[name] = _py_logical_values(value)
            continue
        except RLogicalValueError:
            metadata[name] = value

    for name in metadata:
        try_eval_metadata(metadata, name)

    if "eval" in metadata and not is_active(".Rmd", metadata):
        del metadata["eval"]

    return metadata.get("language") or language, metadata

