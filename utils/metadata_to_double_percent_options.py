
def metadata_to_double_percent_options(metadata, plain_json):
    """Metadata to double percent lines"""
    text = []
    if "title" in metadata:
        text.append(metadata.pop("title"))
    if "cell_depth" in metadata:
        text.insert(0, "%" * metadata.pop("cell_depth"))
    if "cell_type" in metadata:
        text.append("[{}]".format(metadata.pop("region_name", metadata.pop("cell_type"))))
    return metadata_to_text(" ".join(text), metadata, plain_json=plain_json)

