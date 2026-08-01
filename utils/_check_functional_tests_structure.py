
def _check_functional_tests_structure(
    directory: Path, max_file_per_directory: int
) -> None:
    """Check if test directories follow correct file/folder structure.

    Ignore underscored directories or files.
    """
    if Path(directory).stem.startswith("_"):
        return

    files: set[Path] = set()
    dirs: set[Path] = set()

    def _get_files_from_dir(
        path: Path, violations: list[tuple[Path, int]]
    ) -> list[Path]:
        """Return directories and files from a directory and handles violations."""
        files_without_leading_underscore = list(
            p
            for p in path.iterdir()
            if not (p.stem.startswith("_") or (p.is_file() and p.suffix != ".py"))
        )
        if len(files_without_leading_underscore) > max_file_per_directory:
            violations.append((path, len(files_without_leading_underscore)))
        return files_without_leading_underscore

    def walk(path: Path) -> Iterator[Path]:
        violations: list[tuple[Path, int]] = []
        violations_msgs: set[str] = set()
        parent_dir_files = _get_files_from_dir(path, violations)
        error_msg = (
            "The following directory contains too many functional tests files:\n"
        )
        for _file_or_dir in parent_dir_files:
            if _file_or_dir.is_dir():
                yield _file_or_dir.resolve()
                try:
                    yield from walk(_file_or_dir)
                except AssertionError as e:
                    violations_msgs.add(str(e).replace(error_msg, ""))
            else:
                yield _file_or_dir.resolve()
        if violations or violations_msgs:
            _msg = error_msg
            for offending_file, number in violations:
                _msg += f"- {offending_file}: {number} when the max is {max_file_per_directory}\n"
            for error_msg in violations_msgs:
                _msg += error_msg
            raise AssertionError(_msg)

    # Collect all sub-directories and files in directory
    for file_or_dir in walk(directory):
        if file_or_dir.is_dir():
            dirs.add(file_or_dir)
        elif file_or_dir.suffix == ".py":
            files.add(file_or_dir)

    directory_does_not_exists: list[tuple[Path, Path]] = []
    misplaced_file: list[Path] = []
    for file in files:
        possible_dir = file.parent / file.stem.split("_")[0]
        if possible_dir.exists():
            directory_does_not_exists.append((file, possible_dir))
        # Exclude some directories as they follow a different structure
        if (
            not len(file.parent.stem) == 1  # First letter sub-directories
            and file.parent.stem not in IGNORED_PARENT_DIRS
            and file.parent.parent.stem not in IGNORED_PARENT_PARENT_DIRS
        ):
            if not file.stem.startswith(file.parent.stem):
                misplaced_file.append(file)

    if directory_does_not_exists or misplaced_file:
        msg = "The following functional tests are disorganized:\n"
        for file, possible_dir in directory_does_not_exists:
            msg += (
                f"- In '{directory}', '{file.relative_to(directory)}' "
                f"should go in '{possible_dir.relative_to(directory)}'\n"
            )
        for file in misplaced_file:
            msg += (
                f"- In '{directory}', {file.relative_to(directory)} should go in a directory"
                f" that starts with the first letters"
                f" of '{file.stem}' (not '{file.parent.stem}')\n"
            )
        raise AssertionError(msg)

