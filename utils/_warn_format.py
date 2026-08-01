
def _warn_format():
    warnings.warn(
        """Non-JSON file support in nbformat is deprecated since nbformat 1.0.
    Use nbconvert to create files of other formats.""",
        stacklevel=2,
    )

