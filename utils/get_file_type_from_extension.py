
def get_file_type_from_extension(extension: str) -> FileType:
    for file_type, extensions in FILE_EXTENSIONS.items():
        if extension.lower() in extensions:
            return file_type

    raise ValueError(f"Unknown file type for extension: {extension}")

