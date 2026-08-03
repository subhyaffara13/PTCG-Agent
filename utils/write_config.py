from pathlib import Path


def write_config(path: Path, content: str | None = None) -> None:
    if path.suffix == ".toml":
        if content is None:
            content = "[tool.mypy]\nstrict = true"
        path.write_text(content)
    else:
        if content is None:
            content = "[mypy]\nstrict = True"
        path.write_text(content)

