
def check_auto_ext(fmt, metadata, option):
    """Replace the auto extension with the actual file extension, and raise a ValueError if it cannot be determined"""
    if fmt["extension"] != ".auto":
        return fmt

    auto_ext = auto_ext_from_metadata(metadata)
    if auto_ext:
        fmt = fmt.copy()
        fmt["extension"] = auto_ext
        return fmt

    raise ValueError(
        "The notebook does not have a 'language_info' metadata. "
        "Please replace 'auto' with the actual language extension in the {} option (currently {}).".format(
            option, short_form_one_format(fmt)
        )
    )

