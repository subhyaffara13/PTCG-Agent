
def get_file_extension_from_mime_type(mime_type: str) -> str:
    for file_type, mime in FILE_MIME_TYPES.items():
        if mime.lower() == mime_type.lower():
            return FILE_EXTENSIONS[file_type][0]
    raise ValueError(f"Unknown extension for mime type: {mime_type}")

