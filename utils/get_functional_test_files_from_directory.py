import os
from pathlib import Path


def get_functional_test_files_from_directory(
    input_dir: Path | str,
    max_file_per_directory: int = REASONABLY_DISPLAYABLE_VERTICALLY,
) -> list[FunctionalTestFile]:
    """Get all functional tests in the input_dir."""
    suite = []

    _check_functional_tests_structure(Path(input_dir), max_file_per_directory)

    for dirpath, dirnames, filenames in os.walk(input_dir):
        if dirpath.endswith("__pycache__"):
            continue
        dirnames.sort()
        filenames.sort()
        for filename in filenames:
            if filename != "__init__.py" and filename.endswith(".py"):
                suite.append(FunctionalTestFile(dirpath, filename))
    return suite

