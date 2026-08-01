
def metadata_to_text(language_or_title, metadata=None, plain_json=False):
    """Write the cell metadata in the format key=value"""
    # Was metadata the first argument?
    if metadata is None:
        metadata, language_or_title = language_or_title, metadata

    metadata = {key: metadata[key] for key in metadata if key not in _JUPYTEXT_CELL_METADATA}
    text = [language_or_title] if language_or_title else []
    if language_or_title is None:
        if "title" in metadata and "{" not in metadata["title"] and "=" not in metadata["title"]:
            text.append(metadata.pop("title"))

    if plain_json:
        if metadata:
            text.append(dumps(metadata))
    else:
        for key in metadata:
            if key == "incorrectly_encoded_metadata":
                text.append(metadata[key])
            elif metadata[key] is None:
                text.append(key)
            else:
                text.append(f"{key}={dumps(metadata[key])}")
    return " ".join(text)

