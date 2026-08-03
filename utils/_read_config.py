from pathlib import Path


def _read_config(config_file: Path) -> TestFileOptions:
    config = configparser.ConfigParser()
    config.read(str(config_file))
    source_roots = config.get("testoptions", "source_roots", fallback=None)
    return {
        "source_roots": source_roots.split(",") if source_roots else [],
        "output_formats": config.get(
            "testoptions", "output_formats", fallback="mmd"
        ).split(","),
        "command_line_args": shlex.split(
            config.get("testoptions", "command_line_args", fallback="")
        ),
    }

