import json

def _package_payload_config(
    archive_writer: PT2ArchiveWriter,
    payload_config: schema.PayloadConfig,
    config_file: str,
) -> None:
    """
    Save the payload config as json file in the archive.
    """
    archive_writer.write_string(
        config_file, json.dumps(_dataclass_to_dict(payload_config))
    )

