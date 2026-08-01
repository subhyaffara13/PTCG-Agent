
def _raise_file_not_found(path: str, err: Exception | None) -> NoReturn:
    msg = path
    if isinstance(err, RepositoryNotFoundError):
        msg = f"{path} (repository not found)"
    elif isinstance(err, RevisionNotFoundError):
        msg = f"{path} (revision not found)"
    elif isinstance(err, HFValidationError):
        msg = f"{path} (invalid repository id)"
    raise FileNotFoundError(msg) from err

