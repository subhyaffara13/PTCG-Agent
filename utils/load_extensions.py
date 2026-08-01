
def load_extensions(
    environment: "Environment",
    extensions: t.Sequence[t.Union[str, t.Type["Extension"]]],
) -> t.Dict[str, "Extension"]:
    """Load the extensions from the list and bind it to the environment.
    Returns a dict of instantiated extensions.
    """
    result = {}

    for extension in extensions:
        if isinstance(extension, str):
            extension = t.cast(t.Type["Extension"], import_string(extension))

        result[extension.identifier] = extension(environment)

    return result

