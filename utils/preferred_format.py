
def preferred_format(incomplete_format, preferred_formats):
    """Return the preferred format for the given extension"""
    incomplete_format = long_form_one_format(incomplete_format)
    if "format_name" in incomplete_format:
        return incomplete_format

    for fmt in long_form_multiple_formats(preferred_formats):
        if (
            (
                incomplete_format["extension"] == fmt["extension"]
                or (
                    fmt["extension"] == ".auto"
                    and incomplete_format["extension"] not in [".md", ".markdown", ".Rmd", ".ipynb"]
                )
            )
            and incomplete_format.get("suffix") == fmt.get("suffix", incomplete_format.get("suffix"))
            and incomplete_format.get("prefix") == fmt.get("prefix", incomplete_format.get("prefix"))
        ):
            fmt.update(incomplete_format)
            return fmt

    return incomplete_format

