
def get_unsafe_globals_in_checkpoint(f: FileLike) -> list[str]:
    """Returns a list of strings of functions/classes in a ``torch.save`` object that are not safe for ``weights_only``.

    For a given function or class ``f``, the corresponding string will be of the form
    ``{f.__module__}.{f.__name__}``.

    This function will return any GLOBALs in the checkpoint that are not in the set marked safe
    for ``weights_only`` (either via :func:`add_safe_globals` or :class:`safe_globals` context or
    allowlisted by ``torch`` by default).

    .. note::
        This function will statically disassemble the pickle file in the checkpoint.
        The implication is any classes dynamically pushed onto the stack during unpickling
        will not be included in the output.

    Args:
        f: File-like object or string containing the checkpoint object saved via ``torch.save``

    Returns:
        A list of strings of pickle GLOBALs in the checkpoint that are not allowlisted for ``weights_only``.
    """
    default_safe_globals_strings = set(
        _weights_only_unpickler._get_allowed_globals().keys()
    )
    user_safe_global_strings = set(
        _weights_only_unpickler._get_user_allowed_globals().keys()
    )
    safe_global_strings = default_safe_globals_strings.union(user_safe_global_strings)

    with _open_file_like(f, "rb") as opened_file:
        if not _is_zipfile(opened_file):
            raise ValueError("Expected input to be a checkpoint returned by torch.save")
        with _open_zipfile_reader(opened_file) as zip_file:
            if _is_torchscript_zip(zip_file):
                raise ValueError(
                    "Expected input to be a checkpoint returned by torch.save but got a torchscript checkpoint"
                )
            data_file = io.BytesIO(zip_file.get_record("data.pkl"))
            all_globals = _weights_only_unpickler.get_globals_in_pkl(data_file)
            return list(all_globals.difference(safe_global_strings))

