
def _create_file_store(params: RendezvousParameters) -> FileStore:
    # If a user specifies an endpoint, we treat it as a path to a file.
    if params.endpoint:
        path = params.endpoint
    else:
        try:
            # The temporary file is readable and writable only by the user of
            # this process.
            _, path = tempfile.mkstemp()
        except OSError as exc:
            raise RendezvousError(
                "The file creation for C10d store has failed. See inner exception for details."
            ) from exc

    try:
        store = FileStore(path)
    except (ValueError, RuntimeError) as exc:
        raise RendezvousConnectionError(
            "The connection to the C10d store has failed. See inner exception for details."
        ) from exc

    return store

