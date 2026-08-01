
def update_metadata_from_rmd_options(name, value, metadata, use_runtools=False):
    """Map the R Markdown cell visibility options to the Jupyter ones"""
    if use_runtools:
        for rmd_option, jupyter_options in _RMARKDOWN_TO_RUNTOOLS_OPTION_MAP:
            if name == rmd_option[0] and value == rmd_option[1]:
                for opt_name, opt_value in jupyter_options:
                    metadata[opt_name] = opt_value
                return True
    else:
        for rmd_option, tag in _RMARKDOWN_TO_JUPYTER_BOOK_MAP:
            if name == rmd_option[0] and value == rmd_option[1]:
                metadata.setdefault("tags", []).append(tag)
                return True
    return False

