from typing import Any

def _streaming_save(
    obj: object,
    f: BufferedIOBase,
    pickle_module: Any = pickle,
    pickle_protocol: int = DEFAULT_PROTOCOL,
) -> None:
    """
    Save the object to a file-like object in a streaming fashion compatible with
    network sockets.

    This behaves similarly to :func:`torch.save` with a few notable differences:

    * A non-seekable file like object can be used when loading.
    * No forwards/backwards compatibility is provided for the serialization
      format. This is only intended to be used with a single version of PyTorch
      with transient storage (i.e. sockets or temp files).
    * mmap is not supported

    See :func:`torch.save` for more details on specific arguments.
    """

    zip_file = _PseudoZipFile()
    _save(
        obj,
        zip_file=zip_file,
        pickle_module=pickle_module,
        pickle_protocol=pickle_protocol,
        _disable_byteorder_record=False,
    )
    zip_file.write_to(f)

