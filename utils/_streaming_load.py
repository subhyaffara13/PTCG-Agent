
def _streaming_load(
    f: BufferedIOBase,
    map_location: MAP_LOCATION = None,
    pickle_module: Any = None,
    *,
    weights_only: bool = True,
    **pickle_load_args: Any,
) -> object:
    """
    Load the object from a file-like object in a streaming fashion compatible with
    network sockets.

    See :func:`_streaming_save` for more details about the streaming behavior.

    See :func:`torch.load` for more details on specific arguments.
    """
    if weights_only:
        if pickle_module is not None:
            raise RuntimeError(
                "Can not safely load weights when explicit pickle_module is specified"
            )
        pickle_module = _weights_only_unpickler
    else:
        if pickle_module is None:
            pickle_module = pickle

    if "encoding" not in pickle_load_args:
        pickle_load_args["encoding"] = "utf-8"

    zip_file = _PseudoZipFile()
    zip_file.read_from(f)
    return _load(
        zip_file=zip_file,
        map_location=map_location,
        pickle_module=pickle_module,
        **pickle_load_args,
    )

