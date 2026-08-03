import os

def is_pt2_package(serialized_model: bytes | str) -> bool:
    """
    Check if the serialized model is a PT2 Archive package.
    """
    try:
        with zipfile.ZipFile(
            io.BytesIO(serialized_model)
            if isinstance(serialized_model, bytes)
            else serialized_model
        ) as zip_reader:
            root_folder = zip_reader.namelist()[0].split(os.path.sep)[0]
            archive_format_path = f"{root_folder}/{ARCHIVE_FORMAT_PATH}"
            if archive_format_path in zip_reader.namelist():
                return zip_reader.read(archive_format_path) == b"pt2"
    except Exception:
        logger.info("Model is not a PT2 package")
    return False

