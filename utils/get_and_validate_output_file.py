from pathlib import Path


def get_and_validate_output_file() -> tuple[bool, Path]:
    """Make sure that the output file is correct."""
    to_file = validate_yes_no("Do you want to write the output to a file?", "no")

    if not to_file:
        return False, Path()

    # pylint: disable-next=bad-builtin
    file_name = Path(input("What should the file be called: "))
    if file_name.exists():
        overwrite = validate_yes_no(
            f"{file_name} already exists. Are you sure you want to overwrite?", "no"
        )

        if not overwrite:
            return False, file_name
        return True, file_name

    return True, file_name

