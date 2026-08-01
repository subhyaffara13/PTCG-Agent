
def metadata_to_rmd_options(language, metadata, use_runtools=False):
    """Convert language and metadata information to their rmd representation"""
    options = (language or "R").lower()
    if "name" in metadata:
        options += " " + metadata["name"] + ","
        del metadata["name"]
    if use_runtools:
        for rmd_option, jupyter_options in _RMARKDOWN_TO_RUNTOOLS_OPTION_MAP:
            if all([metadata.get(opt_name) == opt_value for opt_name, opt_value in jupyter_options]):
                options += " {}={},".format(rmd_option[0], "FALSE" if rmd_option[1] is False else rmd_option[1])
                for opt_name, _ in jupyter_options:
                    metadata.pop(opt_name)
    else:
        for rmd_option, tag in _RMARKDOWN_TO_JUPYTER_BOOK_MAP:
            if tag in metadata.get("tags", []):
                options += " {}={},".format(rmd_option[0], "FALSE" if rmd_option[1] is False else rmd_option[1])
                metadata["tags"] = [i for i in metadata["tags"] if i != tag]
                if not metadata["tags"]:
                    metadata.pop("tags")
    for opt_name in metadata:
        opt_value = metadata[opt_name]
        opt_name = opt_name.strip()
        if opt_name == "active":
            options += f' {opt_name}="{str(opt_value)}",'
        elif isinstance(opt_value, bool):
            options += " {}={},".format(opt_name, "TRUE" if opt_value else "FALSE")
        elif isinstance(opt_value, list):
            options += " {}={},".format(
                opt_name,
                "c({})".format(", ".join([f'"{str(v)}"' for v in opt_value])),
            )
        elif isinstance(opt_value, str):
            if opt_value.startswith("#R_CODE#"):
                options += f" {opt_name}={opt_value[8:]},"
            elif '"' not in opt_value:
                options += f' {opt_name}="{opt_value}",'
            else:
                options += f" {opt_name}='{opt_value}',"
        else:
            options += f" {opt_name}={str(opt_value)},"
    if not language:
        options = options[2:]
    return options.strip(",").strip()

