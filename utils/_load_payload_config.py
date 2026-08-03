import json

def _load_payload_config(
    archive_reader: PT2ArchiveReader,
    config_file: str,
) -> schema.PayloadConfig:
    """
    Load and parse a payload config from the archive.
    """
    return _dict_to_dataclass(
        schema.PayloadConfig,
        json.loads(archive_reader.read_string(config_file)),
    )

