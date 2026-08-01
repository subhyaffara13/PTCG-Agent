
def get_file_mime_type_from_extension(extension: str) -> str:
    file_type = get_file_type_from_extension(extension)
    return get_file_mime_type_for_file_type(file_type)

