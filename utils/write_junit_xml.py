import os

def write_junit_xml(
    dt: float,
    serious: bool,
    messages_by_file: dict[str | None, list[str]],
    path: str,
    version: str,
    platform: str,
) -> None:
    xml = _generate_junit_contents(dt, serious, messages_by_file, version, platform)

    # creates folders if needed
    xml_dirs = os.path.dirname(os.path.abspath(path))
    os.makedirs(xml_dirs, exist_ok=True)

    with open(path, "wb") as f:
        f.write(xml.encode("utf-8"))

