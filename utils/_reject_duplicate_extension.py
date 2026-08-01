
def _reject_duplicate_extension(
    extension: Extension[ExtensionType],
    extensions: list[Extension[ExtensionType]],
) -> None:
    # This is quadratic in the number of extensions
    for e in extensions:
        if e.oid == extension.oid:
            raise ValueError("This extension has already been set.")

