from pathlib import Path


def get_functional_test_files(
    root_directory: Path,
) -> list[FunctionalPyreverseTestfile]:
    """Get all functional test files from the given directory."""
    test_files = []
    for path in root_directory.rglob("*.py"):
        if path.stem.startswith("_"):
            continue
        config_file = path.with_suffix(".rc")
        if config_file.exists():
            test_files.append(
                FunctionalPyreverseTestfile(
                    source=path, options=_read_config(config_file)
                )
            )
        else:
            test_files.append(
                FunctionalPyreverseTestfile(
                    source=path,
                    options={
                        "source_roots": [],
                        "output_formats": ["mmd"],
                        "command_line_args": [],
                    },
                )
            )
    return test_files

